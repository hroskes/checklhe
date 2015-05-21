#ifndef event_h
#define event_h
class Particle;
class Momentum;
class Frame;
#include <iostream>
#include "particle.h"
#include "momentum.h"

class Event
{
    private:
        TList *_momenta;
        TList *_particlelist;
        TList *_frames;
        Frame *_labframe;
        bool _finished;
    public:
        Event();
        ~Event();
        Particle *particle(TString line);
        Particle *particle(int id, int status, int mother1, int mother2, double px, double py, double pz, double e);
        Particle *getparticle(int position);
        void finished();
        void print();
        Momentum *momentum(double px, double py, double pz, double e);
        Frame *frame();
};
#endif
