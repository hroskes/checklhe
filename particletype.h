#ifndef particletype_h
#define particletype_h
#include "TString.h"

class ParticleType
{
    protected:
        int _id;
    public:
        ParticleType();
        virtual ~ParticleType();
        ParticleType(int id);
        void init(int id);
        virtual TString str();
        double PDGmass();
        double charge();
        ParticleType operator-();
        bool islepton();
        bool isZ();
        bool ishiggs();
        bool isquark();
        bool isjet();
        ClassDef(ParticleType, 1);
};
#endif
