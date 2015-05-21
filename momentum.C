#ifndef momentum_C
#define momentum_C

#include "momentum.h"

Momentum::Momentum() : Momentum(0, 0, 0, 0, 0)
{}

Momentum::Momentum(double px, double py, double pz, double e, TList *momentumlist)
 : TLorentzVector(px, py, pz, e), _momentumlist(momentumlist)
{
    if (_momentumlist != 0)
        _momentumlist->Add(this);
}

Momentum::~Momentum()
{}

Frame::Frame(TList *framelist, TList *momentumlist) : _framelist(framelist), _momentumlist(momentumlist)
{
    _x = new Momentum(1, 0, 0, 0, momentumlist);
    _y = new Momentum(0, 1, 0, 0, momentumlist);
    _z = new Momentum(0, 0, 1, 0, momentumlist);
    _t = new Momentum(0, 0, 0, 1, momentumlist);
   if (framelist != 0)
      framelist->Add(this);
}

Frame::~Frame()
{
    if (_momentumlist == 0)
    {
        delete _x;
        delete _y;
        delete _z;
        delete _t;
    }
    else
    {
        //they are in momentumlist, and so they are deleted by the event
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
