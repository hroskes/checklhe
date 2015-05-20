#ifndef momentum_h
#define momentum_h

#include "TLorentzVector.h"
#include "TList.h"

class Momentum : public TLorentzVector
{
    private:
        TList *_list;
    public:
        Momentum(double px, double py, double pz, double e, TList *list);
        Momentum();
        virtual ~Momentum();
        ClassDef(Momentum, 1); //momentum
};

class Frame : public TObject
{
    private:
        TList *_list;
        TLorentzVector *_x;
        TLorentzVector *_y;
        TLorentzVector *_z;
        TLorentzVector *_t;
    public:
        Frame(TList *list);
        ~Frame();
        TLorentzVector *x();
        TLorentzVector *y();
        TLorentzVector *z();
        TLorentzVector *t();
        ClassDef(Frame, 1); //frame
};
#endif
