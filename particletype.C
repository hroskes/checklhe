#ifndef particletype_C
#define particletype_C

#include "particletype.h"

ParticleType::ParticleType()
{
    _id = 0;
}
ParticleType::ParticleType(int id)
{
    _id = id;
}
void ParticleType::init(int id)
{
    if (_id == 0)
        _id = id;
    else
        assert(0);
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
