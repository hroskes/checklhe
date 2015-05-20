#ifndef event_C
#define event_C

#include <vector>
#include "event.h"
#include "particle.C"
#include "momentum.C"

Event::Event() : _momenta(new TList()), _particlelist(new TList()), _frames(new TList()), _labframe(frame()), _finished(false)
{
    _particlelist->Add(0); //so that the indices line up with the LHE mother indices
    _frames->SetOwner();
    _momenta->SetOwner();
    //_particlelist->DoNOTSetOwner().  Particle is a subclass of Momentum,
    // so the particles are deleted in the momentum loop.
}

Event::~Event()
{
    delete _frames;
    delete _momenta;
    delete _particlelist;
}

void Event::addparticle(Particle *p)
{
    _particlelist->Add(p);
}

Particle *Event::particle(TString line)
{
    return new Particle(line, _particlelist);  //added to _particlelist by the particle's constructor
}

Particle *Event::particle(int id, int mother1, int mother2, double px, double py, double pz, double e)
{
    return new Particle(id, mother1, mother2, px, py, pz, e, _particlelist);  //added to _particlelist by the particle's constructor
}

Particle *Event::getparticle(int position)
{
    return (Particle*)_particlelist->At(position);
}

void Event::finished()
{
    _finished = true;
}

void Event::addmomentum(Momentum *m)
{
    _momenta->Add(m);
}

Momentum *Event::momentum(double px, double py, double pz, double e)
{
    return new Momentum(px, py, pz, e, _momenta);  //added to _momenta by the momentum's constructor
}

void Event::addframe(Frame *f)
{
    _frames->Add(f);
}

Frame *Event::frame()
{
    return new Frame(_frames);
}

#endif
