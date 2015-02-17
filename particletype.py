from fractions import Fraction

class ParticleType:
    def __init__(self, particleorid):
        self.__id = int(particleorid)
        if id < 0 and self in globalvariables.neutralbosons:
            self.__id = -self.__id

    def id(self):
        return self.__id
    def __str__(self):
        particlename = {1: "d",
                        2: "u",
                        3: "s",
                        4: "c",
                        5: "b",
                        6: "t",
                        11: "e-",
                        12: "nue",
                        13: "mu-",
                        14: "numu",
                        15: "tau-",
                        16: "nutau",
                        21: "g",
                        22: "gamma",
                        23: "Z",
                        24: "W+",
                        25: "H"}
        if self.id() < 0:
            result = str(-self)
            if "-" in result:
                result = result.replace("-","+")
            elif "+" in result:
                result = result.replace("+","-")
            elif self in globalvariables.neutrinos:
                result = result.replace("nu","nubar")
            elif self in globalvariables.quarks:
                result = result + "bar"
            else:
                raise ValueError("Invalid particle id! " + str(self.id()))
            return result
        try:
            return particlename[self.id()]
        except KeyError:
            raise ValueError("Invalid particle id! " + str(self.id()))

    def __neg__(self):
        return ParticleType(-self.id())

    def charge(self):
        if self.id() < 0:
            return -(-self).charge()
        if self in globalvariables.downtypequarks:
            return Fraction(-1, 3)
        if self in globalvariables.uptypequarks:
            return Fraction(2, 3)
        if self in globalvariables.leptons:
            return -1
        if self in globalvariables.neutrinos:
            return 0
        if self in globalvariables.neutralbosons:
            return 0
        if self in globalvariables.W:
            return 1
        raise ValueError("Invalid particle id " + str(self.id()))

    def baryonnumber(self):
        if self.id() < 0:
            return -(-self).baryonnumber()
        if self in globalvariables.quarks:
            return Fraction(1,3)
        return 0
    def leptonnumber(self, generation):
        if self.id() < 0:
            return -(-self).leptonnumber(generation)
        if (generation == 1 and self.id() in [11, 12]
         or generation == 2 and self.id() in [13, 14]
         or generation == 3 and self.id() in [15, 16]):
            return 1
        return 0

    def __hash__(self):
        return self.id()
    def __eq__(self, other):
        return self.id() == other.id()
    def __ne__(self, other):
        return not self == other
    def __int__(self):
        return self.id()

import globalvariables
