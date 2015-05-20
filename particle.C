#ifndef particle_C
#define particle_C

#include <vector>
#include <stdexcept>
#include "particle.h"
#include "particletype.C"
#include "momentum.C"
#include "helperfunctions.C"

Particle::Particle(int id, int mother1, int mother2, double px, double py, double pz, double e, TList *list) :
    ParticleType(id), Momentum(px, py, pz, e, list), _list(list)
{
    _motherindices = std::make_pair(mother1, mother2);
}

Particle::Particle(TString line, TList *list) :
    ParticleType(), Momentum(0, 0, 0, 0, list), _list(list)
{
    std::vector<int> intdata;
    std::vector<double> doubledata;
    for (int i = 0; i < 6; i++)
    {
        TString part = nPart(i, line);
        if (! TString(part.Strip(TString::kLeading, '-')).IsDigit())
            throw std::runtime_error((line + "\nis a bad particle line!").Data());
        intdata.push_back(part.Atoi());
    }
    for (int i = 6; i < 13; i++)
    {
        TString part = nPart(i, line);
        if (! part.IsFloat())
            throw std::runtime_error((line + "\nis a bad particle line!").Data());
        doubledata.push_back(part.Atof());
    }

    _id = intdata[0];
    init(_id);
    _status = intdata[1];
    _motherindices = std::make_pair(intdata[2], intdata[3]);
    _mothers = std::make_pair((Particle*)0, (Particle*)0);
    SetPxPyPzE(doubledata[0], doubledata[1], doubledata[2], doubledata[3]);

    list->Add(this);
}

void Particle::setmothers()
{
    if ((_mothers.first || ! _motherindices.first) && (_mothers.second || ! _motherindices.second))
        return;
    _mothers = std::make_pair((Particle*)_list->At(_motherindices.first), (Particle*)_list->At(_motherindices.second));
    if (_mothers.first)
    {
        _mothers.first->setmothers();
        _mothers.first->addkid(this);
    }
    if (_mothers.second && _mothers.second != _mothers.first)
    {
        _mothers.second->setmothers();
        _mothers.second->addkid(this);
    }
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
    for (unsigned int i = 0; i < _kids.size(); i++)
        if (_kids[i] == kid)
            return;
    _kids.push_back(kid);
}

ParticleType Particle::particletype()
{
    return ParticleType(_id);
}
#endif
