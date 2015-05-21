#ifndef event_C
#define event_C

#include <vector>
#include "event.h"
#include "particle.C"
#include "momentum.C"

Event::Event() : _momenta(new TList()), _particlelist(new TList()), _frames(new TList()), _labframe(frame()), _finished(false)
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

#endif
