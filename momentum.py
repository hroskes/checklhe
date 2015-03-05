import config
import ROOT
from math import copysign, acos

momenta = []

def newevent():
    del momenta[:]

class Momentum(ROOT.TLorentzVector):
    def __init__(self, px, py, pz, E):
        super(Momentum, self).__init__(px, py, pz, E)
        momenta.append(self)

    def __eq__(self, other):
        return (self-other).P()**2 + (self-other).E()**2 < config.momentumtolerance
    def __ne__(self, other):
        return not (self == other)
    def __str__(self):
        return "(%s, %s, %s, %s)" % (self.Px(), self.Py(), self.Pz(), self.E())

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
