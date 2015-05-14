import usefulstuff
import config
import ROOT
from math import acos, atan2, copysign, log, tan

class Momentum(ROOT.TLorentzVector):
    def __init__(self, px, py, pz, E):
        self.px = px
        self.py = py
        self.pz = pz
        self.e = E
        self.m = copysign(abs(E**2-px**2-py**2-pz**2)**0.5,E**2-px**2-py**2-pz**2)
        self.superinited = False

    def Px(self):
        return self.px
    def Py(self):
        return self.py
    def Pz(self):
        return self.pz
    def E(self):
        return self.e
    def M(self):
        return self.m
    def P(self):
        return (self.px**2+self.py**2+self.pz**2)**.5
    def Pt(self):
        return (self.px**2+self.py**2)**.5
    def Theta(self):
        return atan2(self.Pt(), self.pz)
    def Eta(self):
        return -log(tan(self.Theta()/2))
    def Phi(self):
        return atan2(self.py, self.px)
    def Rapidity(self):
        return 1/2*log((self.e+self.pz)/(self.e-self.pz))

    def Vect(self):
        self.superinit()
        return super(Momentum, self).Vect()
    def BoostVector(self):
        self.superinit()
        return super(Momentum, self).BoostVector()
    def Boost(self, *args):
        self.superinit()
        return super(Momentum, self).Boost(*args)
    def Rotate(self, *args):
        self.superinit()
        return super(Momentum, self).Rotate(*args)

    def __eq__(self, other):
        return (self-other).P()**2 + (self-other).E()**2 < config.momentumtolerance**2
    def __ne__(self, other):
        return not (self == other)
    def __neg__(self):
        return Momentum(-self.Px(), -self.Py(), -self.Pz(), -self.E())
    def __add__(self, other):
        return Momentum(self.Px()+other.Px(), self.Py()+other.Py(), self.Pz()+other.Pz(), self.E()+other.E())
    def __sub__(self, other):
        return self + (-other)
    def __str__(self):
        return "(%s, %s, %s, %s)" % (self.Px(), self.Py(), self.Pz(), self.E())

    def superinit(self):
        if not self.superinited:
            super(Momentum, self).__init__(self.Px(), self.Py(), self.Pz(), self.E())
            self.superinited = True

class Frame(object):
    def __init__(self):
        self.x = Momentum(1, 0, 0, 0)
        self.y = Momentum(0, 1, 0, 0)
        self.z = Momentum(0, 0, 1, 0)
        self.t = Momentum(0, 0, 0, 1)
