import particle
import particletype
import particlecategory
import globalvariables
import config
import momentum
from math import copysign, acos

class Event:
    def __init__(self, particlelist, linenumber):
        self.particlelist = [p for p in particlelist if p is not None]
        self.particlecounter = particle.ParticleCounter(particlelist)
        self.linenumber = linenumber

        self.decaylist = [p for p in self.particlelist if p.status() == 2]
        self.incoming = [p for p in self.particlelist if p.status() == -1]

        globalvariables.anyevent.increment()
        if config.count4levents and self.count(globalvariables.leptons) >= 4:
            globalvariables.any4l.increment()

        self.checkfunctions = []
        if config.checkinvmass:
            self.checkfunctions.append(self.checkinvmass)
        if config.checkPDGmass:
            self.checkfunctions.append(self.checkPDGmass)
        if config.checkmomentum:
            self.checkfunctions.append(self.checkmomentum)
        if config.checkcharge:
            self.checkfunctions.append(self.checkcharge)
        if config.counthiggsdecaytype:
            self.checkfunctions.append(self.checkhiggsdecay)
        if config.countVHdecaytype and self.isVH():
            self.checkfunctions.append(self.checkVdecay)
        if config.checkZZassignment:
            self.checkfunctions.append(self.checkZZassignment)

        self.processfunctions = []
        if config.makedecayanglestree:
            self.processfunctions.append(self.getdecayangles)
        if config.tree:
            self.anythingtofill = False
            self.processfunctions.append(self.filltree)

    def count(self, whattocount):
        return self.particlecounter.count(whattocount)

    def process(self):
        for prcs in self.processfunctions:
            prcs()

    def check(self):
        checks = [chk() for chk in self.checkfunctions]
        return "\n".join([chk for chk in checks if chk])

    def checkinvmass(self):
        results = []
        for p in self.particlelist:
            if abs(p.invmass() - p.lhemass()) >= config.invmasstolerance:
                results.append("Mass is inconsistent! " + str(self.linenumber) + "(" + str(p) + ")\n" +
                               "invariant mass = " + str(p.invmass()) + "\n" +
                               "LHE mass       = " + str(p.lhemass()))
        return "\n".join(results)

    def checkPDGmass(self):
        results = []
        for p in self.particlelist:
            if p in config.checkPDGmasslist:
                if abs(p.lhemass() - p.PDGmass()) >= config.PDGmasstolerance * p.PDGmass():
                    results.append("Mass is wrong! " + str(self.linenumber) + "(" + str(p) + ")\n" +
                                   "PDG mass = " + str(p.PDGmass()) + "\n" +
                                   "LHE mass = " + str(p.lhemass()))
        return "\n".join(results)

    def checkmomentum(self):
        results = []
        for p in self.decaylist:
            mommomentum = p.momentum()
            kidsmomentum = sum([kid.momentum() for kid in p.kids()], momentum.Momentum(0, 0, 0, 0))
            if mommomentum != kidsmomentum:
                results.append("no momentum conservation! " + str(self.linenumber) + "\n" +
                               "mom momentum  = " + str(mommomentum) + "("  + str(p) + ")\n" +
                               "kids momentum = " + str(kidsmomentum) + "(" + ", ".join([str(kid) for kid in p.kids()]) + ")")
        return "\n".join(results)

    def checkcharge(self):
        results = []
        for p in self.decaylist:
            momcharge = p.charge()
            kidscharge = sum([kid.charge() for kid in p.kids()])
            if momcharge != kidscharge:
                results.append("no charge conservation! " + str(self.linenumber) + "\n" +
                               "mom charge  = " + str(momcharge) + "("  + str(p) + ")\n" +
                               "kids charge = " + str(kidscharge) + "(" + ", ".join([str(kid) for kid in p.kids()]) + ")")
        return "\n".join(results)

    def higgs(self):
        higgs = [p for p in self.particlelist if str(p) == "H"]
        if len(higgs) == 0:
            raise IOError("No higgs in event! " + str(self.linenumber))
        if len(higgs) > 1:
            raise IOError("Multiple higgs in event! " + str(self.linenumber))
        return higgs[0]

    def higgsdecay(self, level = None):
        return particle.DecayType(self.higgs(), level).particles()

    def higgsdecaytype(self, level = None):
        return particle.DecayType(self.higgs(), level)

    def checkhiggsdecay(self):
        for family in globalvariables.decayfamiliestoplevel:
            if family.increment(self.higgs()):
                return ""
        return ("unknown decay type! " + str(self.linenumber) + "\n" +
                "H -> " + str(higgsdecay))

    def ishiggs(self):
        return len([p for p in self.particlelist if str(p) == "H"]) == 1


#VH
    def isVH(self):
        return bool(self.getVfromVH())
    def getVfromVH(self):
        immediateproduction = [p for p in self.particlelist if all(parent in self.incoming for parent in p.mothers())]
        counter = particle.ParticleCounter(immediateproduction)
        if counter.count(globalvariables.weakbosons) == 1 and counter.count(globalvariables.higgs) == 1:
            return [p for p in immediateproduction if p in globalvariables.weakbosons][0]
        else:
            return None

    def checkVdecay(self):
        V = self.getVfromVH()
        if V is None:
            return "Not VH event! " + str(self.linenumber)
        Vdecay = particle.DecayType(V)

        categories = None
        if V in globalvariables.W:
            categories = globalvariables.WH.increment(particle.DecayType(V))     #automatically increments the correct decay
        if V in globalvariables.Z:
            categories = globalvariables.ZH.increment(particle.DecayType(V))     #automatically increments the correct decay

        if categories is None:
            assert(0)                                        #Has to be ZH or WH

        if len(categories) == 1:
            return ("unknown V decay type! " + str(self.linenumber) + "\n" +
                    "V -> " + str(Vdecay))

        globalvariables.VH.increment()
        return ""

#conversion

    def filltree(self):
        if self.anythingtofill:
            globalvariables.tree.Fill()

    def isZZ(self):
        return len(self.higgs().kids()) == 2 and all(kid in globalvariables.Z for kid in self.higgs().kids())

    def Z(self, which):
        if not self.isZZ():
            return None
        Zs = self.higgs().kids()
        assert(all(Z in globalvariables.Z for Z in Zs))
        Zs.sort(key = lambda Z: abs(Z.invmass() - Z.PDGmass()))
        return Zs[which - 1]

    def checkZZassignment(self):
        if (self.higgs() not in globalvariables.decayZZ4l
        and self.higgs() not in globalvariables.decayZZ4q
        and self.higgs() not in globalvariables.decayZZ4nu):
            return ""
        assert(len(self.higgs().kids()) == 2)
        Z1 = self.Z(1)
        Z2 = self.Z(2)
        assert(Z1 is not None and Z2 is not None)
        assert(len(Z1.kids()) == len(Z2.kids()) == 2)
        if particle.ParticleCounter(Z1.kids()) != particle.ParticleCounter(Z2.kids()):
            return ""
        Z1kid1 = Z1.kids()[0]
        altZ1kid1 = [kid for kid in Z2.kids() if particletype.ParticleType(kid) == particletype.ParticleType(Z1kid1)]
        Z1kid2 = Z1.kids()[1]
        altZ1kid2 = [kid for kid in Z2.kids() if particletype.ParticleType(kid) == particletype.ParticleType(Z1kid2)]
        if len(altZ1kid1) == len(altZ1kid2) == 0:
            return ""
        elif len(altZ1kid1) == len(altZ1kid2) == 1:
            pass
        else:
            assert(0)
        altZ1kid1 = altZ1kid1[0]
        altZ1kid2 = altZ1kid2[0]

        altZ1momentum = Z1kid1.momentum() + altZ1kid2.momentum()
        altZ2momentum = Z1kid2.momentum() + altZ1kid1.momentum()
        altmass = min(altZ1momentum.M(), altZ2momentum.M(), key = lambda mass: abs(mass - Z1.PDGmass()))
        if abs(altmass - Z1.PDGmass()) < abs(Z1.invmass() - Z1.PDGmass()):
            return ("Alternate Z has closer mass to m_Z than listed Z! " + str(self.linenumber) + "\n" +
                    "listed Z mass    = " + str(Z1.invmass()) + "\n" +
                    "alternate Z mass = " + str(altmass) + "\n")

    def getdecayangles(self):
        globalvariables.costheta1[0] = -999
        globalvariables.costheta2[0] = -999
        globalvariables.Phi[0] = -999

        lab = momentum.Frame()

        Zs = {1: self.Z(1), 2: self.Z(2)}
        if Zs[1] is None or Zs[2] is None:
            return
        leptons = {}
        for Z in (1, 2):
            for sign in (1, -1):
                leptons[(Z, sign)] = [p for p in Zs[Z].kids() if p.id()*sign > 0][0]
        #sign is -charge
        for i in leptons:
            if leptons[i] not in globalvariables.leptons:
                return
        momentum.boosttocom(Zs[1].momentum())
        globalvariables.costheta1[0] = -leptons[(1, 1)].momentum().Vect().Unit().Dot(Zs[2].momentum().Vect().Unit())
        momentum.boosttocom(Zs[2].momentum())
        globalvariables.costheta2[0] = -leptons[(2, 1)].momentum().Vect().Unit().Dot(Zs[1].momentum().Vect().Unit())

        momentum.boosttocom(self.higgs().momentum())
        normal1 = leptons[1, 1].momentum().Vect().Cross(leptons[1, -1].momentum().Vect()).Unit()
        normal2 = leptons[2, 1].momentum().Vect().Cross(leptons[2, -1].momentum().Vect()).Unit()
        globalvariables.Phi[0] = copysign(acos(-normal1.Dot(normal2)),Zs[1].momentum().Vect().Dot(normal1.Cross(normal2)))

        lab.goto()
        self.anythingtofill = True
