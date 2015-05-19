#ifndef momentum_h
#define momentum_h

#include "TLorentzVector.h"
class Event;
#include "event.h"

class Momentum : public TLorentzVector
{
    private:
        Event *_ev;
    public:
        Momentum(double px, double py, double pz, double e, Event *ev);
        ClassDef(Momentum, 1); //name
};

class Frame
{
    private:
        TLorentzVector *_x;
        TLorentzVector *_y;
        TLorentzVector *_z;
        TLorentzVector *_t;
    public:
        Frame(Event *ev);
        TLorentzVector *x();
        TLorentzVector *y();
        TLorentzVector *z();
        TLorentzVector *t();
};
#endif
