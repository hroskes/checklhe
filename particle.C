#ifndef particle_C
#define particle_C

#include <vector>
#include "particle.h"
#include "particletype.C"
#include "momentum.C"
#include "event.C"

class BadParticleLineException: public runtime_error {
    public:
        BadParticleLineException(TString particleline)
            : line(particleline), runtime_error(particleline)
        {}

    virtual const char* what() const throw()
    {
        return line + "\nis an invalid particle line!";
    }

    private:
        TString line;
};

Particle::Particle(int id, int mother1, int mother2, double px, double py, double pz, double e, Event *ev) :
    Momentum(ev, px, py, pz, e), ParticleType(id), _ev(ev)
{}

Particle::Particle(TString line, Event *ev) :
    Momentum(ev, 0, 0, 0, 0), ParticleType(), _ev(ev)
{
    std::vector<int> intdata;
    std::vector<double> doubledata;
    for (int i = 0; i < 6; i++)
    {
        TString part = nPart(i, line);
        if (! part.IsDigit())
            throw BadParticleLineException(line);
        intdata.push_back(part.Atoi());
    }
    for (int i = 6; i < 13; i++)
    {
        TString part = nPart(i, line);
        if (! part.IsFloat())
            throw BadParticleLineException(line);
        doubledata.push_back(part.Atof());
    }

    _id = intdata[0];
    init(_id);
    _status = intdata[1];
    _motherindices = make_pair(intdata[2], intdata[3]);
    _mothers = make_pair((Particle*)0, (Particle*)0);
    SetPxPyPzE(doubledata[0], doubledata[1], doubledata[2], doubledata[3]);

    ev->addparticle(this);
}

void Particle::setmothers()
{
    if ((mothers.first || ! motherindices.first) && (mothers.last || ! motherindices.last))
        continue;
    _mothers = make_pair(_ev->particlelist[_motherindices.first], _ev->particlelist[_motherindices.last]);
    _mothers.first->setmothers();
    _mothers.last->setmothers();
    _mothers.first->addkid(this);
    _mothers.last->addkid(this);
}

bool Particle::iskidof(Particle *potentialmother)
{
    return (_mothers.first == potentialmother || _mothers.second == potentialmother);
}
bool Particle::ismotherof(Particle *potentialkid)
{
    return potentialkid->iskidof(this);
}
void Particle::addkid(Particle *kid)
{
    for(std::vector<Particle*>::iterator it = _kids.begin(); it != _kids.end(); ++it)
        if ((*it) == kid)
            return;
    _kids->push_back(kid);
}

ParticleType Particle::particletype()
{
    return ParticleType(_id);
}
#endif
