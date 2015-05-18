#include "momentum.h"

Momentum::Momentum(Event *ev, double px, double py, double pz, double e)
 : TLorentzVector(px, py, pz, e), _ev(ev)
{
    if (_ev != 0)
        _ev->momenta.push_back(this);
}
