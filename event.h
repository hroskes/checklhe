#ifndef event_h
#define event_h
class Particle;
class Momentum;
class Frame;
#include <vector>
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
        Momentum *_partonVBF1, *_partonVBF2;
    public:
        Event(int linenumber);
        ~Event();
        Particle *particle(TString line);
        Particle *particle(int id, int status, int mother1, int mother2, double px, double py, double pz, double e);
        Particle *getparticle(int position);
        void finished();
        void print();
        Momentum *momentum(const TLorentzVector& v);
        Momentum *momentum(double px, double py, double pz, double e);
        Frame *frame();
        //Lorentz transformations
        void boost(double x, double y, double z);
        void boost(const TVector3& b);
        void boosttocom(TLorentzVector *tocom);
        void rotate(double a, const TVector3& v);
        void rotatetozx(TLorentzVector *toz, TLorentzVector *tozx = 0);
        void gotoframe(Frame *f);
        //conversion
        Particle *gethiggs();
        bool isZZ();
        Particle *getZ(int i);
        void getZZmasses(double& mZZ, double& mZ1, double& mZ2);
        void getleptonmomenta(std::vector<double>& leptonpt, std::vector<double>& leptoneta, std::vector<double>& leptonphi, std::vector<double>&leptonmass);
        std::vector<Particle*> getleptons();
        void getleadingleptonmomenta(double& leadingpt, double& leadingeta, double& subleadingpt, double& subleadingeta);
        bool isZZ4f();
        bool isZZ4l();
        int getZZ4lflavor();
        void getZZ4langles(double& costheta1, double& costheta2, double& Phi, double& costhetastar, double& Phi1);
        //VBF
        int njets();
        std::vector<Particle*> getjets();
        void getjetmomenta(std::vector<double>& jetpt, std::vector<double>& jeteta, std::vector<double>& jetphi, std::vector<double>&jetmass);
        Particle *getjet(int i, TString sortbypzorpt);
        Momentum *getpartonVBF(int i, bool uselhepartons = false);
        Momentum *getVVBF(int i, bool uselhepartons = false);
        void getVBFangles(double& costheta1, double& costheta2, double& Phi, double& costhetastar, double& Phi1, double& q2v1, double& q2v2, bool uselhepartons = false);
        //void getVBFangles(double& costheta1, double& costheta2, double& Phi, double& costhetastar, double& Phi1, double& phistar, double& q2v1, double& q2v2, bool uselhepartons = false);
        void getVBFjetvariables(double& mJJ, double& dEta, double& dPhi, double& dR);
};
#endif
