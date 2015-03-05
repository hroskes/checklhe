from fractions import Fraction
from collections import Counter
import momentum
import itertools
import particletype
import particlecategory
import globalvariables
import config

particlelist = []

def newevent():
    del particlelist[:]
    momentum.newevent()
    particlelist.append(None)

class Particle(particletype.ParticleType):
    def __init__(self, line):
        data = line.split()
        if len(data) < 13:
            raise ValueError("This line is not a valid particle line.  Not enough entries.")
        super(Particle, self).__init__(int(data[0]))
        self.__status = int(data[1])
        self.__momentum = momentum.Momentum(float(data[6]), float(data[7]), float(data[8]), float(data[9]))
        self.__lhemass = float(data[10])
        particlelist.append(self)
        self.__mothers = [particlelist[int(data[2])], particlelist[int(data[3])]]
        self.__kids = []
        for particle in particlelist[1:]:
            if particle in self.mothers():
                particle.kids().append(self)

    def __eq__(self, other):
       return self is other
    def __ne__(self, other):
       return not self == other

    def status(self):
        return self.__status
    def mothers(self):
        return self.__mothers
    def kids(self):
        return self.__kids
    def momentum(self):
        return self.__momentum
    def invmass(self):
        return self.__momentum.M()
    def lhemass(self):
        return self.__lhemass

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
    def __eq__(self, other):
        return hash(self) == hash(other)
    def __ne__(self, other):
        return not self == other

class DecayType(ParticleCounter):
    def __init__(self, particle, level = None):
        try:
            decayparticles = particle.particles   #see if it's itself a decaytype
        except AttributeError:
            decayparticles = [particle]
        done = False
        i = 0
        while not done and (level is None or i < level):
            i += 1
            done = True
            for p in decayparticles[:]:
                if p.status() == 2:
                    done = False
                    decayparticles.remove(p)
                    decayparticles += p.kids()
        self.particles = decayparticles
        super(DecayType, self).__init__(decayparticles)

class EventCount(object):
    def __init__(self, name = "", subcategories = None):
        self.name = name
        self.subcategories = []
        if subcategories is not None:
            self.subcategories = subcategories

    def __hash__(self):
        return hash(self.name)

    def printcount(self):
        count = globalvariables.eventcounter[self]
        total = globalvariables.eventcounter[globalvariables.anyevent]
        if count > 0:
            joiner = "\n    "
            result = "%s %s events (%s%%)" % (count, self.name, 100.0*count/total)
            result += joiner
        else:
            result = ""
            joiner = "\n"
        for subcategory in self.subcategories:
            result += joiner.join([line for line in subcategory.printcount().split("\n")])
        return result.rstrip(" ")

    def increment(self):
        globalvariables.eventcounter[self] += 1

class DecayFamily(EventCount, set):
    def __init__(self, decaytypes, charge = None, baryonnumber = None, leptonnumber = (None, None, None), name = "", subcategories = None, Csymmetric = True):
        finallist = []
        secondarylist = []

        for d in decaytypes:
            try:
                secondarylist.append(ParticleCounter(d))
            except TypeError:
                for tple in itertools.product(*[particlecategory.ParticleCategory(p, Csymmetric) for p in d]):
                    secondarylist.append(ParticleCounter(tple))

        for d in secondarylist:
            if charge is None or charge == d.charge():
                if baryonnumber is None or d.baryonnumber() == baryonnumber:
                    if all(leptonnumber[i] is None or d.leptonnumber(i+1) == leptonnumber[i] for i in range(3)):
                        finallist.append(d)

        set.__init__(self, finallist)
        EventCount.__init__(self, name, subcategories)

    def increment(self, decay):
        incremented = []
        if len(self) == 0 or decay in self:
            super(DecayFamily, self).increment()
            incremented.append(self)
        for subcategory in self.subcategories:
            subincremented = subcategory.increment(decay)
            incremented += subincremented
            #to check
            if (self not in incremented) and subincremented:
                raise RuntimeError("Subcategory '%s' of category '%s' is filled even though its parent is not!" % (subincremented[0].name, self.name))
        return incremented

    def __contains__(self, other):
        if super(DecayFamily, self).__contains__(ParticleCounter(other)):
            return True
        try:
            newother = DecayType(other, 1)
        except AttributeError:
            return False
        if newother != other:
            return self.__contains__(newother)
        else:
            return False
    def __hash__(self):
        return hash((self.name, tuple(d for d in self)))
    def __str__(self):
        return ";    ".join(str(decay) for decay in self)
