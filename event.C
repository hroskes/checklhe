#ifndef event_C
#define event_C

#include <vector>
#include "event.h"
#include "particle.C"
#include "momentum.C"

Event::Event(int linenumber) : _momenta(new TList()), _particlelist(new TList()), _frames(new TList()), _labframe(frame()), _finished(false), _linenumber(linenumber)
{
    new Particle(_particlelist); //placeholder so that the indices line up with the LHE mother indices
    _frames->SetOwner();
    _momenta->SetOwner();
    //_particlelist->DoNOTSetOwner().  Particle is a subclass of Momentum,
    // so the particles are deleted when _momenta is
}

Event::~Event()
{
    delete _frames;
    delete _momenta;
    delete _particlelist;
}

Particle *Event::particle(TString line)
{
    if (_finished) assert(0);
    return new Particle(line, _particlelist, _momenta);  //added to _particlelist by the particle's constructor
}

Particle *Event::particle(int id, int status, int mother1, int mother2, double px, double py, double pz, double e)
{
    if (_finished) assert(0);
    return new Particle(id, status, mother1, mother2, px, py, pz, e, _particlelist, _momenta);  //added to _particlelist by the particle's constructor
}

Particle *Event::getparticle(int position)
{
    return (Particle*)_particlelist->At(position);
}

void Event::finished()
{
    if (_finished) assert(0);
    _finished = true;
    //i = 1 is correct - the first item in the list is a placeholder
    //so that the indices in the list match up with the LHE mother indices
    for (int i = 1; i < _particlelist->GetSize(); i++)
        ((Particle*)(_particlelist->At(i)))->setmothers();
}

void Event::print()
{
    if (!_finished) assert(0);
    for (int i = 1; i < _particlelist->GetSize(); i++)
        std::cout << ((Particle*)(_particlelist->At(i)))->str() << std::endl;
}

Momentum *Event::momentum(const TLorentzVector& v)
{
    return new Momentum(v, _momenta);  //added to _momenta by the momentum's constructor
}

Momentum *Event::momentum(double px, double py, double pz, double e)
{
    return new Momentum(px, py, pz, e, _momenta);  //added to _momenta by the momentum's constructor
}

Frame *Event::frame()
{
    return new Frame(_frames, _momenta);
}

///////////////////////////////////
//    Lorentz transformations    //
///////////////////////////////////

void Event::boost(double x, double y, double z)
{
    for (int i = 0; i < _momenta->GetSize(); i++)
        ((Momentum*)(_momenta->At(i)))->Boost(x, y, z);
}

void Event::boost(const TVector3 &b)
{
    for (int i = 0; i < _momenta->GetSize(); i++)
        ((Momentum*)(_momenta->At(i)))->Boost(b);
}

void Event::boosttocom(TLorentzVector *tocom)
{
    TVector3 b = -tocom->BoostVector();
    boost(b);
}

void Event::rotate(double a, const TVector3& v)
{
    for (int i = 0; i < _momenta->GetSize(); i++)
        ((Momentum*)(_momenta->At(i)))->Rotate(a, v);
}

void Event::rotatetozx(TLorentzVector *toz, TLorentzVector *tozx)
{
    TVector3 toz3 = toz->Vect();
    TVector3 tozx3(0, 0, 0);
    if (tozx)
        tozx3 = tozx->Vect();
    double angle = acos(toz3.Unit().Z());
    TVector3 axis = toz3.Unit().Cross(TVector3(0, 0, 1));
    if (axis == TVector3(0, 0, 0))  //if thisOneGoesToZ cross z = 0, it's in the -z direction and angle = pi, so rotate around y
        axis = TVector3(0, 1, 0);   //                               or it's in the +z direction and angle = 0, so it doesn't matter.
    rotate(angle, axis);
    if (tozx)
    {
        tozx3.Rotate(angle, axis);  //Since tozx3 was decoupled from tozx before the first rotation, this is ok whether or not tozx is in momenta
        angle = -tozx3.Phi();
        axis = TVector3(0,0,1);
        rotate(angle,axis);
    }
}

void Event::gotoframe(Frame *f)
//f should have been created through frame() so that its unit vectors are in _momenta
//or bad things will happen
{
    boosttocom(f->t());
    rotatetozx(f->z(), f->x());
}

////////////////////
//   conversion   //
////////////////////

Particle *Event::gethiggs()
{
    Particle *h = 0;
    for (int i = 1; i < _particlelist->GetSize(); i++)
        if (((Particle*)_particlelist->At(i))->ishiggs())
        {
            if (h)
                throw std::runtime_error((TString("Multiple higgs in event! ") += _linenumber).Data());
            else
                h = (Particle*)_particlelist->At(i);
        }
    return h;
}

bool Event::isZZ()
{
    Particle *h = gethiggs();
    if (!h || h->nkids() != 2)
        return false;
    return (h->getkid(0)->isZ() && h->getkid(1)->isZ());
}

Particle *Event::getZ(int i)
//i should be 1 or 2
//1: the Z with mass closer to mZ
//2: the Z with mass further from mZ
{
    if (!isZZ() || (i != 1 && i != 2)) return 0;
    Particle *h = gethiggs();
    Particle *Za = h->getkid(0);
    Particle *Zb = h->getkid(1);
    if ((fabs(Za->M() - Za->PDGmass()) < fabs(Zb->M() - Zb->PDGmass())) ^ (i-1))
        return Za;
    else
        return Zb;
}

bool Event::isZZ4l()
{
    if (!isZZ())
        return false;
    for (int i = 1; i <= 2; i++)
    {
        Particle *Z = getZ(i);
        if (Z->nkids() != 2)
            return false;
        for (int j = 0; j <= 1; j++)
            if (!Z->getkid(j)->islepton())
                return false;
    }
    return true;
}

int Event::getZZ4lflavor()
{
    //consistent with older readOutAngles scripts
    if (!isZZ4l())
        return -999;
    Particle *Z1 = getZ(1);
    Particle *Z2 = getZ(2);
    int flavor1 = fabs(Z1->getkid(0)->id());
    int flavor2 = fabs(Z2->getkid(0)->id());
    switch (flavor1+3*flavor2)
    {
        case 44: return 0; //4e
        case 50: return 3; //2e2mu
        case 56: return 4; //2e2tau
        case 46: return 6; //2mu2e
        case 52: return 1; //4mu
        case 58: return 5; //2mu2tau
        case 48: return 7; //2tau2e
        case 54: return 8; //2tau2mu
        case 60: return 2; //4tau
        default: assert(0); return -999;
    }
}

void Event::getZZmasses(double& mZZ, double& mZ1, double& mZ2)
{
    mZZ = -999;
    mZ1 = -999;
    mZ2 = -999;
    Particle *h = gethiggs();
    if (h)
        mZZ = h->M();
    if (isZZ())
    {
        Particle *Z1 = getZ(1);
        Particle *Z2 = getZ(2);
        mZ1 = Z1->M();
        mZ2 = Z2->M();
    }
}

void Event::getZZ4langles(double& costheta1, double& costheta2, double& Phi, double& costhetastar, double& Phi1)
{
    costheta1 = -999;
    costheta2 = -999;
    Phi = -999;
    costhetastar = -999;
    Phi1 = -999;
    if (!isZZ4l()) return;
    Particle *Z1 = getZ(1);
    Particle *Z2 = getZ(2);
    Particle *l1m = getZ(1)->getkid(0);
    Particle *l1p = getZ(1)->getkid(1);
    Particle *l2m = getZ(2)->getkid(0);
    Particle *l2p = getZ(2)->getkid(1);
    if (!l1m || !l1p || !l2m || !l2p) assert(0);
    if (l1m->charge() > 0)
    {
        Particle *temp = l1m;
        l1m = l1p;
        l1p = temp;
    }
    if (l2m->charge() > 0)
    {
        Particle *temp = l2m;
        l2m = l2p;
        l2p = temp;
    }
    if (l1m->charge() > 0)
    {
        Particle *temp = l1m;
        l1m = l1p;
        l1p = temp;
    }
    if (!(l1m->charge() == -1 && l1p->charge() == 1 && l2m->charge() == -1 && l2p->charge() == 1))
        assert(0); //return;

    boosttocom(Z1);
    costheta1 = -l1m->Vect().Unit().Dot(Z2->Vect().Unit());

    boosttocom(Z2);
    costheta2 = -l2m->Vect().Unit().Dot(Z1->Vect().Unit());

    gotoframe(_labframe);
    boosttocom(gethiggs());
    TVector3 normal1 = l1m->Vect().Cross(l1p->Vect()).Unit();
    TVector3 normal2 = l2m->Vect().Cross(l2p->Vect()).Unit();
    Phi = std::copysign(acos(-normal1.Dot(normal2)), Z1->Vect().Dot(normal1.Cross(normal2)));

    TVector3 beamaxis(0, 0, 1);
    costhetastar = Z1->Vect().Unit().Dot(beamaxis);
    TVector3 normal3 = beamaxis.Cross(Z1->Vect()).Unit();
    Phi1 = std::copysign(acos(normal1.Dot(normal3)), Z1->Vect().Dot(normal1.Cross(normal3)));

}

int Event::njets()
{
    int n = 0;
    for (int i = 1; i < _particlelist->GetSize(); i++)
    {
        Particle *p = (Particle*)_particlelist->At(i);
        if (p->isjet())
            n++;
    }
    return n;
}

vector<Particle*> Event::getjets()
{
    vector<Particle*> jets;
    for (int i = 1; i < _particlelist->GetSize(); i++)
    {
        Particle *p = (Particle*)_particlelist->At(i);
        if (!p->isjet())
            continue;
        jets.push_back(p);
    }
    return jets;
}

void Event::getjetmomenta(vector<double>& jetpt, vector<double>& jeteta, vector<double>& jetphi, vector<double>&jetmass)
{
    jetpt.clear();
    jeteta.clear();
    jetphi.clear();
    jetmass.clear();
    gotoframe(_labframe);
    for (int i = 1; i < _particlelist->GetSize(); i++)
    {
        Particle *p = (Particle*)_particlelist->At(i);
        if (!p->isjet())
            continue;
        jetpt.push_back(p->Pt());
        jeteta.push_back(p->Eta());
        jetphi.push_back(p->Phi());
        jetmass.push_back(p->M());
    }
}

Particle *Event::getjet(int i, TString sortbypzorpt)
{
    sortbypzorpt.ToLower();
    if ((i != 1 && i != 2) || njets() == 0)
        return 0;
    if (njets() == 1)
    {
        if (i == 1)
            return getjets()[0];
        else
            return 0;
    }
    vector<Particle*> jets = getjets();
    Particle *jet1 = jets[0];
    Particle *jet2 = jets[1];
    double pzorpt, pzorpt1, pzorpt2;
    for (unsigned int j = 1; j < jets.size(); i++)
    {
        if (sortbypzorpt == "pt")
        {
            pzorpt = jets[j]->Pt();
            pzorpt1 = jet1->Pt();
            pzorpt2 = jet2->Pt();
        }
        else if (sortbypzorpt == "pz")
        {
            pzorpt = jets[j]->Pz();
            pzorpt1 = jet1->Pz();
            pzorpt2 = jet2->Pz();
        }
        else
            throw std::invalid_argument((TString("getjet's second argument needs to be either pz or pt, not ") += sortbypzorpt).Data());
        if (pzorpt > pzorpt1)
        {
            jet2 = jet1;
            jet1 = jets[j];
        }
        else if (pzorpt > pzorpt2 && jets[i] != jet1)
            jet2 = jets[j];
    }
    if (i == 1)
        return jet1;
    else if (i == 2)
        return jet2;
    else
        return 0;
}

Momentum *Event::getpartonVBF(int i, bool uselhepartons)
{
    if (njets() < 2 || !gethiggs() || (i != 1 && i != 2)) return 0;
    if (uselhepartons)
    {
        Particle *p1 = 0;
        Particle *p2 = 0;
        for (int j = 1; j < _particlelist->GetSize(); j++)
        {
            Particle *p = (Particle*)_particlelist->At(j);
            if (p->status() != -1)
                continue;
            if (p1 == 0 || p->Pz() > p1->Pz())
            {
                p2 = p1;
                p1 = p;
            }
            else if (p2 == 0)
                p2 = p;
            else
                throw std::runtime_error((TString("Too many incoming particles in event! ") += _linenumber).Data());
        }
        if (i == 1)
            return p1;
        else if (i == 2)
            return p2;
    }
    if (!_partonVBF1 || !_partonVBF2)
    {
        Frame *bkpframe = frame();
        Particle *jet1 = getjet(1, "pz");
        Particle *jet2 = getjet(2, "pz");
        Momentum *HJJ = momentum(*(gethiggs()) + *jet1 + *jet2);
        Momentum *HJJ_T = momentum(HJJ->Px(), HJJ->Py(), 0, HJJ->E());
        boosttocom(HJJ_T);
        boosttocom(HJJ);     //sequential boosts to preserve the z direction
        _partonVBF1 = momentum(0, 0,  HJJ->E()/2, HJJ->E()/2);
        _partonVBF2 = momentum(0, 0, -HJJ->E()/2, HJJ->E()/2);
        gotoframe(bkpframe);
    }
    if (i == 1)
        return _partonVBF1;
    else if (i == 2)
        return _partonVBF2;
    return 0;
}

#endif
