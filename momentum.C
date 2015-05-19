#ifndef momentum_C
#define momentum_C

#include "momentum.h"
#include "event.C"

Momentum::Momentum() : Momentum(0, 0, 0, 0, 0)
{}

Momentum::Momentum(double px, double py, double pz, double e, Event *ev)
 : TLorentzVector(px, py, pz, e), _ev(ev)
{
    if (_ev != 0)
        _ev->addmomentum(this);
}

Momentum::~Momentum()
{}

Frame::Frame(Event *ev) : _ev(ev)
{
    _x = new Momentum(1, 0, 0, 0, ev);
    _y = new Momentum(0, 1, 0, 0, ev);
    _z = new Momentum(0, 0, 1, 0, ev);
    _t = new Momentum(0, 0, 0, 1, ev);
   ev->addframe(this);
}

Frame::~Frame()
{
    if (_ev == 0)
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

TLorentzVector *Frame::x()
{
    return _x;
}
TLorentzVector *Frame::y()
{
    return _y;
}
TLorentzVector *Frame::z()
{
    return _z;
}
TLorentzVector *Frame::t()
{
    return _t;
}
#endif
