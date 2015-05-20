#ifndef momentum_C
#define momentum_C

#include "momentum.h"

Momentum::Momentum() : Momentum(0, 0, 0, 0, 0)
{}

Momentum::Momentum(double px, double py, double pz, double e, TList *list)
 : TLorentzVector(px, py, pz, e), _list(list)
{
    if (_list != 0)
        _list->Add(this);
}

Momentum::~Momentum()
{}

Frame::Frame(TList *list) : _list(list)
{
    _x = new Momentum(1, 0, 0, 0, list);
    _y = new Momentum(0, 1, 0, 0, list);
    _z = new Momentum(0, 0, 1, 0, list);
    _t = new Momentum(0, 0, 0, 1, list);
   list->Add(this);
}

Frame::~Frame()
{
    if (_list == 0)
    {
        delete _x;
        delete _y;
        delete _z;
        delete _t;
    }
    else
    {
        //they are in list->_momenta, and so they are deleted by list's destructor
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
