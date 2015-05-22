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

#endif
