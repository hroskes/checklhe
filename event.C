#ifndef event_C
#define event_C

#include "event.h"

#ifndef CMSSW
#include "particle.C"
#include "momentum.C"
#endif

#include "TMath.h"
#include <vector>
#include <assert.h>

static bool onlyZZ4l = false;  //calculate angles only for ZZ->4l, not e.g. ZZ->2l2nu

Event::Event(int linenumber) : _momenta(new TList()), _particlelist(new TList()), _frames(new TList()), _labframe(frame()), _finished(false), _linenumber(linenumber), _partonVBF1(0), _partonVBF2(0)
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

void Event::getleptonmomenta(std::vector<double>& leptonpt, std::vector<double>& leptoneta, std::vector<double>& leptonphi, std::vector<double>&leptonmass)
{
    leptonpt.clear();
    leptoneta.clear();
    leptonphi.clear();
    leptonmass.clear();
    gotoframe(_labframe);
    for (int i = 1; i < _particlelist->GetSize(); i++)
    {
        Particle *p = (Particle*)_particlelist->At(i);
        if (!p->islepton())
            continue;
        leptonpt.push_back(p->Pt());
        leptoneta.push_back(p->Eta());
        leptonphi.push_back(p->Phi());
        leptonmass.push_back(p->M());
    }
}

std::vector<Particle*> Event::getleptons()
{
    std::vector<Particle*> leptons;
    for (int i = 1; i < _particlelist->GetSize(); i++)
    {
        Particle *p = (Particle*)_particlelist->At(i);
        if (!p->islepton())
            continue;
        leptons.push_back(p);
    }
    return leptons;
}

void Event::getleadingleptonmomenta(double& leadingpt, double& leadingeta, double& subleadingpt, double& subleadingeta)
{
    Particle *leading = 0, *subleading = 0;
    std::vector<Particle*> leptons = getleptons();
    for (unsigned int i = 0; i < leptons.size(); i++)
    {
        Particle *p = leptons[i];
        if (!leading || p->Pt() >= leading->Pt())
            leading = p;
    }
    for (unsigned int i = 0; i < leptons.size(); i++)
    {
        Particle *p = leptons[i];
        if (p == leading) continue;
        if (!subleading || p->Pt() >= subleading->Pt())
            subleading = p;
    }
    leadingpt = leading->Pt();
    leadingeta = leading->Eta();
    subleadingpt = subleading->Pt();
    subleadingeta = subleading->Eta();
}

bool Event::isZZ4f()
{
    if (!isZZ())
        return false;
    for (int i = 1; i <= 2; i++)
    {
        Particle *Z = getZ(i);
        if (Z->nkids() != 2)
            return false;
    }
    return true;
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
    if ((!isZZ4l() && onlyZZ4l) || !isZZ4f()) return;
    Particle *Z1 = getZ(1);
    Particle *Z2 = getZ(2);
    Particle *l1m = getZ(1)->getkid(0);
    Particle *l1p = getZ(1)->getkid(1);
    Particle *l2m = getZ(2)->getkid(0);
    Particle *l2p = getZ(2)->getkid(1);
    if (!l1m || !l1p || !l2m || !l2p) assert(0);
    if (l1m->id() < 0)
    {
        Particle *temp = l1m;
        l1m = l1p;
        l1p = temp;
    }
    if (l2m->id() < 0)
    {
        Particle *temp = l2m;
        l2m = l2p;
        l2p = temp;
    }
    if (!(l1m->id() > 0 && l1p->id() < 0 && l2m->id() > 0 && l2p->id() < 0))
        assert(0);

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

///////////////////////////////////
//              VBF              //
///////////////////////////////////

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

std::vector<Particle*> Event::getjets()
{
    std::vector<Particle*> jets;
    for (int i = 1; i < _particlelist->GetSize(); i++)
    {
        Particle *p = (Particle*)_particlelist->At(i);
        if (!p->isjet())
            continue;
        jets.push_back(p);
    }
    return jets;
}

void Event::getjetmomenta(std::vector<double>& jetpt, std::vector<double>& jeteta, std::vector<double>& jetphi, std::vector<double>&jetmass)
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
    std::vector<Particle*> jets = getjets();
    Particle *jet1 = jets[0];
    Particle *jet2 = jets[1];
    double pzorpt, pzorpt1, pzorpt2;
    for (unsigned int j = 1; j < jets.size(); j++)
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
            throw std::invalid_argument((TString("getjet's second argument needs to be either pz or pT, not ") += sortbypzorpt).Data());
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

Momentum *Event::getVVBF(int i, bool uselhepartons)
{
    Momentum *parton = getpartonVBF(i, uselhepartons);
    Momentum *jet = getjet(i, "pz");
    if (parton == 0)
        return 0;
    return momentum(*jet-*parton);
}

void Event::getVBFangles(double& costheta1, double& costheta2, double& Phi, double& costhetastar, double& Phi1, double& q2v1, double& q2v2, bool uselhepartons)
{
    gotoframe(_labframe);
    Particle *higgs = gethiggs();
    Particle *Z1 = getZ(1);
    Particle *jet1 = getjet(1, "pz");
    Particle *jet2 = getjet(2, "pz");
    Momentum *parton1 = getpartonVBF(1, uselhepartons);
    Momentum *parton2 = getpartonVBF(2, uselhepartons);
    Momentum *V1 = getVVBF(1, uselhepartons);
    Momentum *V2 = getVVBF(2, uselhepartons);

    q2v1 = V1->M2();
    q2v2 = V2->M2();

    boosttocom(higgs);
    costheta1 = -V1->Vect().Dot(jet1->Vect())/jet1->Vect().Mag()/V1->Vect().Mag();
    costheta2 = -V2->Vect().Dot(jet2->Vect())/jet2->Vect().Mag()/V2->Vect().Mag();
    costhetastar = -V1->Vect().Dot(Z1->Vect())/V1->Vect().Mag()/Z1->Vect().Mag();

    TVector3 tmp1 = parton1->Vect().Cross(jet1->Vect()).Unit();
    TVector3 tmp2 = parton2->Vect().Cross(jet2->Vect()).Unit();
    TVector3 tmp3 = V1->Vect().Cross(Z1->Vect()).Unit();

    double cosPhi = tmp1.Dot(tmp2);
    double sgnPhi = tmp1.Cross(tmp2).Dot(V1->Vect());
    double cosPhi1 = -tmp1.Dot(tmp3);
    double sgnPhi1 = tmp1.Dot(Z1->Vect());
    Phi = TMath::Sign(acos(cosPhi),sgnPhi);            //TMath::Sign(a,b) = |a|*(b/|b|)
    Phi1 = TMath::Sign(acos(cosPhi1),sgnPhi1);
}

/*
This gives incorrect values of phistar as compared to my code from earlier this year.  I don't know why yet.
void Event::getVBFangles(double& costheta1, double& costheta2, double& Phi, double& costhetastar, double& Phi1, double& phistar, double& q2v1, double& q2v2, bool uselhepartons)
{
    gotoframe(_labframe);
    getVBFangles(costheta1, costheta2, Phi, costhetastar, Phi1, q2v1, q2v2, uselhepartons);

    gotoframe(_labframe);
    Particle *higgs = gethiggs();
    Particle *jet1 = getjet(1, "pz");
    Particle *jet2 = getjet(2, "pz");

    Momentum *hjj = momentum(*higgs+*jet1+*jet2);
    rotatetozx(_labframe->z(), hjj);
    TVector3 pTboostvector = -hjj->BoostVector();
    pTboostvector.SetZ(0);
    boost(pTboostvector);

    phistar = higgs->Phi();
}
*/

void Event::getVBFjetvariables(double& mJJ, double& dEta, double& dPhi, double& dR)
{
    gotoframe(_labframe);
    Particle *jet1 = getjet(1, "pT");
    Particle *jet2 = getjet(2, "pT");
    mJJ = (*jet1+*jet2).M();
    dEta = jet1->Eta() - jet2->Eta();
    dPhi = jet1->DeltaPhi(*jet2);
    dR = jet1->DeltaR(*jet2);
}

#endif
