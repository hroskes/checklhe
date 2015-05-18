

ParticleType::ParticleType()
{
    _id = 0;
}
ParticleType::ParticleType(int id)
{
    _id = id;
}
void init(int id)
{
    if (_id == 0)
        _id = id;
    else
        assert(0);
}

ParticleType operator-()
{
    return ParticleType(-_id);
}
