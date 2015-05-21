#ifndef particletype_C
#define particletype_C

#include "particletype.h"
#include <assert.h>

ParticleType::ParticleType()
{
    _id = 0;
}
ParticleType::ParticleType(int id)
{
    _id = id;
}
ParticleType::~ParticleType()
{}
void ParticleType::init(int id)
{
    if (_id == 0)
        _id = id;
    else
        assert(0);
}

TString ParticleType::str()
{
    if (_id < 0)
    {
        TString result = (-(*this)).str();
        result.ReplaceAll("-","temp")
              .ReplaceAll("+","-")
              .ReplaceAll("temp","+")
              .ReplaceAll("nu","nubar");
        if (isquark())
            result += "bar";
        return result;
    }
    switch(_id)
    {
        case 1:  return "d";
        case 2:  return "u";
        case 3:  return "s";
        case 4:  return "c";
        case 5:  return "b";
        case 6:  return "t";
        case 11: return "e-";
        case 12: return "nue";
        case 13: return "mu-";
        case 14: return "numu";
        case 15: return "tau-";
        case 16: return "nutau";
        case 21: return "g";
        case 22: return "gamma";
        case 23: return "Z";
        case 24: return "W+";
        case 25: return "H";
        case 32: return "Z'";
        case 39: return "G";
        default: return TString("unknown particle id") += _id;
    }
}

ParticleType ParticleType::operator-()
{
    return ParticleType(-_id);
}

bool ParticleType::islepton()
{
    return (fabs(_id) == 11 || fabs(_id) == 13 || fabs(_id) == 15);
}
bool ParticleType::isZ()
{
    return (_id == 23);
}
bool ParticleType::ishiggs()
{
    return (_id == 25 || _id == 32 || _id == 39);
}
bool ParticleType::isquark()
{
    return (fabs(_id) == 1 || fabs(_id) == 2 || fabs(_id) == 3 || fabs(_id) == 4 || fabs(_id) == 5 || fabs(_id) == 6);
}
bool ParticleType::isjet()
{
    return (fabs(_id) == 1 || fabs(_id) == 2 || fabs(_id) == 3 || fabs(_id) == 4 || fabs(_id) == 5 || _id == 21);
}

#endif
