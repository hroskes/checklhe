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

class Particle(particletype.ParticleType):
    def __init__(self, line):
        data = line.split()
        if len(data) < 13:
            raise ValueError("This line is not a valid particle line.  Not enough entries.")
        super(Particle, self).__init__(int(data[0]))
        self.__status = int(data[1])
        self.__momentum = Momentum(float(data[6]), float(data[7]), float(data[8]), float(data[9]))
        self.__lhemass = float(data[10])
        particlelist.append(self)
        self.__mothers = [particlelist[int(data[2])], particlelist[int(data[3])]]
        self.__kids = []
        for particle in particlelist[1:]:
            if particle in self.mothers():
                particle.kids().append(self)

    def __eq__(self, other):
       return self is other

    def status(self):
        return self.__status
    def mothers(self):
        return self.__mothers
    def kids(self):
        return self.__kids
    def momentum(self):
        return self.__momentum
    def invmass(self):
        return self.__momentum.m()
    def usemass(self):
        return self.invmass()
    def lhemass(self):
        return self.__lhemass

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
        return (self-other).euclideanabs() < globalvariables.momentumtolerance
    def __ne__(self, other):
        return not (self == other)

    def __str__(self):
        return "(%s, %s, %s, %s)" % (self.px(), self.py(), self.pz(), self.E())

class ParticleCounter(Counter):
    def __init__(self, particles):
        try:                    #if particles is another ParticleCounter
            super(ParticleCounter, self).__init__([particletype.ParticleType(p) for p in particles.elements() if p is not None])
        except AttributeError:
            try:                #if it's a list
                super(ParticleCounter, self).__init__([particletype.ParticleType(p) for p in particles if p is not None])
            except TypeError:   #if it's a single particle
                super(ParticleCounter, self).__init__([particletype.ParticleType(particles)])
    def count(self, whattocount):
        return len([p for p in self.elements() if p in whattocount])
    def charge(self):
        return sum([p.charge() for p in self.elements()])
    def baryonnumber(self):
        return sum([p.baryonnumber() for p in self.elements()])
    def leptonnumber(self, generation):
        return sum([p.leptonnumber(generation) for p in self.elements()])
    def __hash__(self):
        return hash(tuple(sorted(hash(p) for p in self.elements())))
    def __str__(self):
        return " ".join(str(p) for p in self.elements())

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
        
class DecayFamily(set):
    def __init__(self, decaytypes, charge = None, baryonnumber = None, leptonnumber = (None, None, None)):
        finallist = []
        secondarylist = []

        for d in decaytypes:
            try:
                secondarylist.append(ParticleCounter(d))
            except TypeError:
                for tple in itertools.product(*[particlecategory.ParticleCategory(p) for p in d]):
                    secondarylist.append(ParticleCounter(tple))

        for d in secondarylist:
            if charge is None or charge == d.charge():
                if baryonnumber is None or d.baryonnumber() == baryonnumber:
                    if all(leptonnumber[i] is None or d.leptonnumber(i+1) == leptonnumber[i] for i in range(3)):
                        finallist.append(d)

        super(DecayFamily, self).__init__(finallist)

    def __contains__(self, other):
        return super(DecayFamily, self).__contains__(ParticleCounter(other))
    def __hash__(self):
        return hash(tuple(d for d in self))
