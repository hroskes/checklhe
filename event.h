#ifndef event_h
#define event_h
#include <vector>
#include "particle.h"
#include "momentum.h"

class Event
{
    private:
        std::vector<Momentum*> _momenta;
        std::vector<Particle*> _particlelist;
        std::vector<Frame*> _frames;
        Frame *labframe;
    public:
        Event();
        ~Event();
        void addparticle(Particle *particle);
        Particle *particle(TString line);
        Particle *particle(int id, int mother1, int mother2, double px, double py, double pz, double e);
        Particle *getparticle(int position)
        void addmomentum(Momentum *momentum);
        Momentum *momentum(double px, double py, double pz, double e);
        void addframe(Frame *frame);
        Frame *frame();
};
#endif
