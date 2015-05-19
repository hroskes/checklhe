#ifndef event_C
#define event_C

#include <vector>
#include "event.h"
#include "particle.C"
#include "momentum.C"

Event::Event()
{}

Event::~Event()
{
    for(std::vector<Particle*>::iterator it = _momenta.begin(); it != _momenta.end(); ++it)
        delete *it;
    //Do NOT do this for _particlelist.  Particle is a subclass of Momentum,
    // so the particles are deleted in the momentum loop.
}

void Event::addparticle(Particle *p)
{
    _particlelist.push_back(p);
}

Particle *Event::particle(TString line)
{
    return new Particle(line, this);  //added to _particlelist by the particle's constructor
}

Particle *Event::particle(int id, int mother1, int mother2, double px, double py, double pz, double e)
{
    return new Particle(id, mother1, mother2, px, py, pz, e, this);  //added to _particlelist by the particle's constructor
}

Particle *Event::getparticle(int position)
{
    return _particlelist[position];
}

void Event::addmomentum(Momentum *m)
{
    _momenta.push_back(m);
}

Momentum *Event::momentum(double px, double py, double pz, double e)
{
    return new Momentum(px, py, pz, e, this);  //added to _momenta by the momentum's constructor
}

void Event::addframe(Frame *f)
{
    _frames.push_back(f);
}

Frame *Event::frame()
{
    return new Frame(this);
}

#endif
