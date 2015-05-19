#ifndef momentum_C
#define momentum_C

#include "momentum.h"
#include "event.C"

Momentum::Momentum(double px, double py, double pz, double e, Event *ev)
 : TLorentzVector(px, py, pz, e), _ev(ev)
{
    if (_ev != 0)
        _ev->addmomentum(this);
}

Frame::~Frame()
{
    if (ev == 0)
    {
        delete _x;
        delete _y;
        delete _z;
        delete _t;
    }
    else
    {
        //they are in ev->_momenta, and so they are deleted by ev's destructor
    }
}

Frame::Frame(Event *ev)
{
    _x = new Momentum(ev, 1, 0, 0, 0);
    _y = new Momentum(ev, 0, 1, 0, 0);
    _z = new Momentum(ev, 0, 0, 1, 0);
    _t = new Momentum(ev, 0, 0, 0, 1);
   ev->addframe(this);
}

TLorentzVector Frame::x()
{
    return _x;
}
TLorentzVector Frame::y()
{
    return _y;
}
TLorentzVector Frame::z()
{
    return _z;
}
TLorentzVector Frame::t()
{
    return _t;
}
#endif
