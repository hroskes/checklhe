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
        Momentum();
        ~Momentum();
        ClassDef(Momentum, 1); //name
};

class Frame
{
    private:
        Event *_ev;
        TLorentzVector *_x;
        TLorentzVector *_y;
        TLorentzVector *_z;
        TLorentzVector *_t;
    public:
        Frame(Event *ev);
        ~Frame();
        TLorentzVector *x();
        TLorentzVector *y();
        TLorentzVector *z();
        TLorentzVector *t();
};
#endif
