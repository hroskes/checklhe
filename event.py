import particle
import particletype
import particlecategory
import globalvariables
import config
import momentum
import vertex
from math import copysign, acos

class Event:
    def __init__(self, particlelist, linenumber):
        self.particlelist = [p for p in particlelist if p is not None]
        self.particlecounter = particle.ParticleCounter(particlelist)
        self.linenumber = linenumber

        self.decaylist = [p for p in self.particlelist if p.status() == 2]
        self.incoming = [p for p in self.particlelist if p.status() == -1]

        globalvariables.anyevent.increment()

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
        if config.checkZZorWWassignment:
            self.checkfunctions.append(self.checkZZorWWassignment)

        self.processfunctions = []
        if config.makedecayanglestree:
            self.processfunctions.append(self.getdecayangles)
        if config.makeZZmassestree:
            self.processfunctions.append(self.getZZmasses)
        if config.count4levents:
            self.processfunctions.append(self.count4l)
        if config.count2l2levents:
            self.processfunctions.append(self.count2l2l)
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
        for v in vertex.vertices.values():
            if v.momentumin() != v.momentumout():
                results.append("no momentum conservation! " + str(self.linenumber) + "\n" +
                               "mom momentum  = " + str(v.momentumin()) + str(v.particlesin()) + "\n" +
                               "kids momentum = " + str(v.momentumout()) + str(v.particlesout()))
        return "\n".join(results)

    def checkcharge(self):
        results = []
        for v in vertex.vertices.values():
            if v.chargein() != v.chargeout():
                results.append("no charge conservation! " + str(self.linenumber) + "\n" +
                               "mom charge  = " + str(v.chargein()) + str(v.particlesin()) + "\n" +
                               "kids charge = " + str(v.chargeout()) + str(v.particlesout()))
        return "\n".join(results)

    def count4l(self):
        if self.count(globalvariables.leptons) >= 4:
            globalvariables.any4l.increment()

    def count2l2l(self):
        leptons = [p for p in self.particlelist if p in globalvariables.leptons]
        flavors = [globalvariables.electrons, globalvariables.muons, globalvariables.taus]
        hasl = {f: {1: 0, -1: 0} for f in flavors}
        for p in leptons:
            for f in flavors:
                if p in f:
                    hasl[f][p.charge()] += 1
        haslplm = [min(hasl[f][1], hasl[f][-1]) for f in flavors]
        if sum(haslplm) >= 2:
            globalvariables.any2l2l.increment()

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
        if self.higgs().status() != 2:
            return ""
        for family in globalvariables.decayfamiliestoplevel:
            if self.higgs() in family:
                family.increment(self.higgs())
                return ""
        return ("unknown decay type! " + str(self.linenumber) + "\n" +
                "H -> " + str(self.higgsdecay()))

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

    def isWW(self):
        return len(self.higgs().kids()) == 2 and all(kid in globalvariables.W for kid in self.higgs().kids())

    def W(self, which):
        if not self.isWW():
            return None
        Ws = self.higgs().kids()
        assert(all(W in globalvariables.W for W in Ws))
        Ws.sort(key = lambda W: abs(W.invmass() - W.PDGmass()))
        return Ws[which - 1]

    def checkZZorWWassignment(self):
        if (self.higgs() not in globalvariables.decayZZ4l
        and self.higgs() not in globalvariables.decayZZ4q
        and self.higgs() not in globalvariables.decayZZ4nu
        and self.higgs() not in globalvariables.decayWW4q
        and self.higgs() not in globalvariables.decayWW2l2nu):
            return ""
        assert(len(self.higgs().kids()) == 2)
        ZorW1 = self.Z(1)
        ZorW2 = self.Z(2)
        if ZorW1 is None and ZorW2 is None:
            ZorW1 = self.W(1)
            ZorW2 = self.W(2)
        assert(ZorW1 is not None and ZorW2 is not None)
        assert(len(ZorW1.kids()) == len(ZorW2.kids()) == 2)
        if particle.ParticleCounter(ZorW1.kids()) != particle.ParticleCounter(ZorW2.kids()):
            return ""
        ZorW1kid1 = ZorW1.kids()[0]
        altZorW1kid1 = [kid for kid in ZorW2.kids() if particletype.ParticleType(kid) == particletype.ParticleType(ZorW1kid1)]
        ZorW1kid2 = ZorW1.kids()[1]
        altZorW1kid2 = [kid for kid in ZorW2.kids() if particletype.ParticleType(kid) == particletype.ParticleType(ZorW1kid2)]
        if len(altZorW1kid1) == len(altZorW1kid2) == 0:
            return ""
        elif len(altZorW1kid1) == len(altZorW1kid2) == 1:
            pass
        else:
            assert(0)
        altZorW1kid1 = altZorW1kid1[0]
        altZorW1kid2 = altZorW1kid2[0]

        altZorW1momentum = ZorW1kid1.momentum() + altZorW1kid2.momentum()
        altZorW2momentum = ZorW1kid2.momentum() + altZorW1kid1.momentum()
        altmass = min(altZorW1momentum.M(), altZorW2momentum.M(), key = lambda mass: abs(mass - ZorW1.PDGmass()))
        if abs(altmass - ZorW1.PDGmass()) < abs(ZorW1.invmass() - ZorW1.PDGmass()):
            return ("Alternate %s has closer mass to m_%s than listed %s! " + str(self.linenumber) + "\n" +
                    "listed %s mass    = " + str(ZorW1.invmass()) + "\n" +
                    "alternate %s mass = " + str(altmass) + "\n") % str(ZorW1)

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

    def getZZmasses(self):
        globalvariables.mZ1[0] = -999
        globalvariables.mZ2[0] = -999
        globalvariables.mH[0] = -999
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
        globalvariables.mZ1[0] = Zs[1].invmass()
        globalvariables.mZ2[0] = Zs[2].invmass()
        globalvariables.mH[0] = self.higgs().invmass()
        self.anythingtofill = True
