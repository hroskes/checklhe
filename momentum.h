#ifndef momentum_h
#define momentum_h

#include "TLorentzVector.h"
#include "TList.h"

class Momentum : public TLorentzVector
{
    private:
        TList *_momentumlist;
    public:
        Momentum(double px, double py, double pz, double e, TList *momentumlist);
        Momentum();
        virtual ~Momentum();
        ClassDef(Momentum, 1); //momentum
};

class Frame : public TObject
{
    private:
        TList *_framelist;
        TList *_momentumlist;
        TLorentzVector *_x;
        TLorentzVector *_y;
        TLorentzVector *_z;
        TLorentzVector *_t;
    public:
        Frame(TList *framelist, TList *momentumlist);
        ~Frame();
        TLorentzVector *x();
        TLorentzVector *y();
        TLorentzVector *z();
        TLorentzVector *t();
        ClassDef(Frame, 1); //frame
};
#endif
