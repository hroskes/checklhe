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

////////////////////
//   conversion   //
////////////////////

Particle *Event::higgs()
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

#endif
