#ifndef particle_h
#define particle_h
class Momentum;
class ParticleType;
#include "momentum.h"
#include "particletype.h"
#include "helperfunctions.h"
#include "TList.h"
class Particle : public ParticleType, public Momentum
{
    private:
        TList *_particlelist;
        TList *_momentumlist;
        int _id;
        int _status;
        int _mothersset;
        std::pair<int, int> _motherindices;
        std::pair<Particle*, Particle*> _mothers;
        std::vector<Particle*> _kids;
    public:
        Particle(int id, int status, int mother1, int mother2, double px, double py, double pz, double e, TList *particlelist = 0, TList *momentumlist = 0);
        Particle(TString line, TList *particlelist = 0, TList *momentumlist = 0);
        Particle(TList *particlelist = 0);   //This one is for "particle 0", which is just a placeholder that is the "mother" of the incoming partons
        int status();
        TString str();
        TString str(bool shortversion);
        bool isjet();
        void setmothers();
        bool iskidof(Particle *potentialmother);
        bool ismotherof(Particle *potentialkid);
        void addkid(Particle *kid);
        unsigned int nkids();
        Particle *getkid(unsigned int i);
        ParticleType particletype();
        ClassDef(Particle, 1);
};
#endif
