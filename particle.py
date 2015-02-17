from fractions import Fraction
from math import copysign
from collections import Counter
import itertools
import particletype
import particlecategory
import globalvariables

particlelist = []

def newevent():
    del particlelist[:]
    particlelist.append(None)

class Particle:
    def __init__(self, line):
        data = line.split()
        if len(data) < 13:
            raise ValueError("This line is not a valid particle line.  Not enough entries.")
        self.__id = int(data[0])
        self.__charge = charge[self.__id]
        self.__status = int(data[1])
        self.__momentum = Momentum(float(data[6]), float(data[7]), float(data[8]), float(data[9]))
        self.__lhemass = float(data[10])
        particlelist.append(self)
        self.__mothers = [particlelist[int(data[2])], particlelist[int(data[3])]]
        self.__kids = []
        for particle in particlelist[1:]:
            if particle in self.mothers():
                particle.kids().append(self)

    def __str__(self):
       return particlename[self.__id]

    def id(self):
        return self.__id
    def charge(self):
        return self.__charge
    def status(self):
        return self.__status
    def mothers(self):
        return self.__mothers
    def kids(self):
        return self.__kids
    def islepton(self):
        return self.id() in leptons
    def ise(self):
        return self.id() in electrons
    def ismu(self):
        return self.id() in muons
    def istau(self):
        return self.id() in taus
    def isquark(self):
        return self.id() in quarks
    def isneutrino(self):
        return self.id() in neutrinos
    def isZ(self):
        return self.id() == 23
    def isH(self):
        return self.id() == 25
    def momentum(self):
        return self.__momentum
    def invmass(self):
        return self.__momentum.m()
    def lhemass(self):
        return self.__lhemass

momentumtolerance = 1e-4
masstolerance = 5e-2

class Momentum:
    def __init__(self, px, py, pz, E):
        self.__px = px
        self.__py = py
        self.__pz = pz
        self.__E = E
        self.__m2 = E**2-px**2-py**2-pz**2
        self.__m = copysign(abs(self.__m2) ** 0.5, self.__m2)

    def px(self):
        return self.__px
    def py(self):
        return self.__py
    def pz(self):
        return self.__pz
    def E(self):
        return self.__E
    def m(self):
        return self.__m
    def __add__(self, other):
        return Momentum(self.px()+other.px(), self.py()+other.py(), self.pz()+other.pz(), self.E()+other.E())
    def __sub__(self, other):
        return Momentum(self.px()-other.px(), self.py()-other.py(), self.pz()-other.pz(), self.E()-other.E())

    def euclideanabs(self):
        return (self.px()**2 + self.py()**2 + self.pz()**2 + self.E()**2) ** 0.5
    def __eq__(self, other):
        return (self-other).euclideanabs() < momentumtolerance
    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return "(%s, %s, %s, %s)" % (self.px(), self.py(), self.pz(), self.E())

class ParticleCounter(Counter):
    def __init__(self, particles):
        try:
            super(ParticleCounter, self).__init__([particletype.ParticleType(p) for p in particles])
        except TypeError:
            super(ParticleCounter, self).__init__([particletype.ParticleType(particles)])     #if particles is a single particle
    def count(self, whattocount):
        return len([p for p in self if p in whattocount])

class DecayType(ParticleCounter):
    def __init__(self, particle):
        decayparticles = particle.kids()
        done = False
        while not done:
            done = True
            for p in decayparticles[:]:
                if p.status() == 2:
                    done = False
                    decayparticles.remove(p)
                    decayparticles += p.kids()
        super(DecayType, self).__init__(decayparticles)
        
class DecayFamily(list):
    def __init__(self, decaytypes):
        l = []
        try:
            for d in decaytypes:
                l.append(ParticleCounter(d))
        except TypeError:
            for d in decaytypes:
                l += [ParticleCounter(tple) for tple in itertools.product(*[particlecategory.ParticleCategory(p) for p in d])]
        super(DecayFamily, self).__init__([d for d in l])

    def __contains__(self, other):
        return super(DecayFamily, self).__contains__(ParticleCounter(other))
