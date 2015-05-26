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
        int _linenumber;
    public:
        Event(int linenumber);
        ~Event();
        Particle *particle(TString line);
        Particle *particle(int id, int status, int mother1, int mother2, double px, double py, double pz, double e);
        Particle *getparticle(int position);
        void finished();
        void print();
        Momentum *momentum(double px, double py, double pz, double e);
        Frame *frame();
        //Lorentz transformations
        void boost(double x, double y, double z);
        void boost(const TVector3& b);
        void boosttocom(TLorentzVector *tocom);
        void rotate(double a, const TVector3& v);
        void rotatetozx(TLorentzVector *toz, TLorentzVector *tozx = 0);
        void gotoframe(Frame *f);
        Particle *gethiggs();
        bool isZZ();
        Particle *getZ(int i);
        void getZZmasses(double& mZZ, double& mZ1, double& mZ2);
        bool isZZ4l();
        int getZZ4lflavor();
        void getZZ4langles(double& costheta1, double& costheta2, double& Phi, double& costhetastar, double& Phi1);
        void getjetmomenta(vector<double>& jetpt, vector<double>& jeteta, vector<double>& jetphi, vector<double>&jetmass);
};
#endif
