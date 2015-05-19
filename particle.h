#ifndef particle_h
#define particle_h
class Momentum;
class ParticleType;
#include "momentum.h"
#include "particletype.h"
class Particle : public ParticleType, public Momentum
{
    private:
        int _ev;
        int _id;
        int _status;
        std::pair<int, int> _motherindices;
        std::pair<Particle*, Particle*> _mothers;
        std::vector<Particle*> _kids;
    public:
        Particle(int id, int mother1, int mother2, double px, double py, double pz, double e, int ev);
        Particle(TString line, int ev);
        void setmothers();
        bool iskidof(Particle *potentialmother);
        bool ismotherof(Particle *potentialkid);
        void addkid(Particle *kid);
        ParticleType particletype();
        ClassDef(Particle, 1);
};
#endif
