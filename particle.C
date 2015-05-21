#ifndef particle_C
#define particle_C

#include <vector>
#include <stdexcept>
#include <iostream>
#include "particle.h"
#include "particletype.C"
#include "momentum.C"
#include "helperfunctions.C"

Particle::Particle(int id, int status, int mother1, int mother2, double px, double py, double pz, double e, TList *particlelist, TList *momentumlist) :
    ParticleType(id), Momentum(px, py, pz, e, momentumlist), _particlelist(particlelist), _id(id), _status(status), _mothersset(false),
                                                             _motherindices(mother1,mother2), _mothers(0,0)
{
    _motherindices = std::make_pair(mother1, mother2);
    if (particlelist != 0)
        particlelist->Add(this);
}

Particle::Particle(TString line, TList *particlelist, TList *momentumlist) :
    ParticleType(), Momentum(0, 0, 0, 0, momentumlist), _particlelist(particlelist), _mothers(0,0)
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

    if (particlelist != 0)
        particlelist->Add(this);
}

Particle::Particle(TList *particlelist) :
    ParticleType(0), Momentum(0, 0, 0, 0, 0), _particlelist(particlelist), _id(0), _status(-1), _mothersset(true),
                                              _motherindices(0,0), _mothers(this,this)
//This one is for "particle 0", which is just a placeholder that is the "mother" of the incoming partons
//Unlike in the python version, we're not checking momentum conservation, so a momentum of 0 is ok
{
    if (particlelist != 0)
        particlelist->Add(this);
}

TString Particle::str()
{
    return str(false);
}

TString Particle::str(bool shortversion)
{
    TString result = ParticleType::str();
    if (shortversion)
        return result;
    result += "    (";
    if (_mothers.first && _mothers.second)
    {
        result += _mothers.first->str(true);
        if (_mothers.first != _mothers.second)
            (result += ",") += _mothers.second->str(true);
    }
    else
    {
        result += _motherindices.first;
        if (_motherindices.first != _motherindices.second)
            (result += ",") += _motherindices.second;
    }
    ((((((((result += ")    (") += Px()) += ",") += Py()) += ",") += Pz()) += ",") += E()) += ")";
    return result;
}

void Particle::setmothers()
{
    if ((_mothers.first || ! _motherindices.first) && (_mothers.second || ! _motherindices.second))
        return;
    _mothers = std::make_pair((Particle*)_particlelist->At(_motherindices.first), (Particle*)_particlelist->At(_motherindices.second));
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
