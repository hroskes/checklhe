#ifndef particletype_h
#define particletype_h

class ParticleType
{
    protected:
        int _id;
    public:
        ParticleType();
        ParticleType(int id);
        void init(int id);
        ParticleType operator-();
        bool islepton();
        bool isZ();
        bool ishiggs();
        bool isquark();
        bool isjet();
};
#endif
