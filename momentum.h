#ifndef momentum_h
#define momentum_h

#include "TLorentzVector.h"
//class Event;
//#include "event.h"

class Momentum : public TLorentzVector
{
    private:
        int _ev;
    public:
        Momentum(double px, double py, double pz, double e, int ev);
        Momentum();
        virtual ~Momentum();
        ClassDef(Momentum, 1); //name
};

class Frame
{
    private:
        int _ev;
        TLorentzVector *_x;
        TLorentzVector *_y;
        TLorentzVector *_z;
        TLorentzVector *_t;
    public:
        Frame(int ev);
        ~Frame();
        TLorentzVector *x();
        TLorentzVector *y();
        TLorentzVector *z();
        TLorentzVector *t();
};
#endif
