import config
import ROOT
from math import copysign, acos

momenta = []

def newevent():
    del momenta[:]

class Momentum(ROOT.TLorentzVector):
    def __init__(self, px, py, pz, E):
        self.px = px
        self.py = py
        self.pz = pz
        self.e = E
        self.m = copysign(abs(E**2-px**2-py**2-pz**2)**0.5,E**2-px**2-py**2-pz**2)
        self.superinited = False
        momenta.append(self)

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
        return (self-other).P()**2 + (self-other).E()**2 < config.momentumtolerance
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

def boostall(x, y = None, z = None):
    if y is None and z is not None or y is not None and z is None:
        raise TypeError
    if y is None and z is None:
        for p in momenta:
            p.Boost(x)
    else:
        for p in momenta:
            p.Boost(x, y, z)

def boosttocom(vect):
    boostvector = -vect.BoostVector()
    boostall(boostvector)

def rotateall(angle, axis):
    for p in momenta:
        p.Rotate(angle, axis)

def rotatetozx(toz, tozx):
    try:
        toz = toz.Vect()
    except AttributeError:
        pass
    try:
        tozx = tozx.Vect()
    except AttributeError:
        pass
    angle = acos(toz.Unit().Z())
    axis = toz.Unit().Cross(ROOT.TVector3(0,0,1))
    if axis == ROOT.TVector3(0,0,0):            #if thisOneGoesToZ cross z = 0, it's in the -z direction and angle = pi, so rotate around y
        axis = ROOT.TVector3(0,1,0)             #                               or it's in the +z direction and angle = 0, so it doesn't matter.
    rotateall(angle,axis)
    if tozx is not None:
        tozx.Rotate(angle,axis)

        angle2 = -tozx.Phi()
        axis2 = ROOT.TVector3(0,0,1)
        rotateall(angle2,axis2)

class Frame(object):
    def __init__(self):
        self.x = Momentum(1, 0, 0, 0)
        self.y = Momentum(0, 1, 0, 0)
        self.z = Momentum(0, 0, 1, 0)
        self.t = Momentum(0, 0, 0, 1)
        
    def goto(self):
        boosttocom(self.t)
        rotatetozx(self.z, self.x)
