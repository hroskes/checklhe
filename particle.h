#ifndef particle_h
#define particle_h
#include "momentum.h"
#include "particletype.h"
class Particle : public ParticleType, public Momentum
{
    private:
        Event *_ev;
        int _id;
        int _status;
        pair<int, int> _motherindices;
        pair<Particle*, Particle*> _mothers;
        std::vector<Particle*> _kids;
    public:
        Particle(int id, int mother1, int mother2, double px, double py, double pz, double e, Event *ev);
        Particle(TString line, Event *ev);
        void setmothers();
        bool iskidof(Particle *potentialmother);
        void addkid(Particle *kid);
        ParticleType particletype();
};
#endif
