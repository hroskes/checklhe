import particle
import particletype
import particlecategory
import globalvariables
import usefulstuff
import config
import momentum
import vertex
import color
import checkdebugoutput
import ROOT
from math import copysign, acos

class Event:
    def __init__(self, linenumber):
        self.linenumber = linenumber
        self.firstline = None
        self.particlelist = usefulstuff.printablelist([None])
        self.vertices = vertex.Vertices()
        self.colors = color.Colors()
        self.done = False

    def setfirstline(self, firstline):
        if self.firstline is not None:
            raise ValueError("The first line for this event is already set to:\n" + self.firstline + "\nand cannot be set again to:\n")
        self.firstline = firstline

    def addparticle(self, particleline):
        if self.firstline is None:
            raise ValueError("The first line for this event has not been set yet!")
        if self.done:
            raise ValueError("finished() has already been called for this event, so no more particles can be added!")
        particle.Particle(particleline, self)

    def finished(self):
        if self.firstline is None:
            raise ValueError("The first line for this event has not been set yet!")
        self.particlelist.remove(None)
        self.particlecounter = particle.ParticleCounter(self.particlelist)

        self.decaylist = [p for p in self.particlelist if p.kids()]
        self.incoming = [p for p in self.particlelist if p.status() == -1]

        globalvariables.globalvariables.anyevent.increment()

        self.miscellaneouschecks = sum(([a + " " + str(self.linenumber) for a in b] for b in self.particlelist[1:].miscellaneouschecks),[])

        self.checkfunctions = []
        if config.checkfirstline:
            self.checkfunctions.append(self.checkfirstline)
        if config.checkstatus:
            self.checkfunctions.append(self.checkstatus)
        if config.checkinvmass:
            self.checkfunctions.append(self.checkinvmass)
        if config.checkPDGmass:
            self.checkfunctions.append(self.checkPDGmass)
        if config.checkmomentum:
            self.checkfunctions.append(self.checkmomentum)
        if config.checkcharge:
            self.checkfunctions.append(self.checkcharge)
        if config.checkcolor:
            self.checkfunctions.append(self.checkcolor)
        if config.checkZZorWWassignment:
            self.checkfunctions.append(self.checkZZorWWassignment)
        if config.counthiggsdecaytype:
            self.checkfunctions.append(self.checkhiggsdecay)
        if config.countVHdecaytype and self.isVH():
            self.checkfunctions.append(self.checkVdecay)

        self.processfunctions = []
        if config.makeZZ4langlestree:
            self.processfunctions.append(self.getZZ4langles)
        if config.makeZZmassestree:
            self.processfunctions.append(self.getZZmasses)
        if config.count4levents:
            self.processfunctions.append(self.count4l)
        if config.count2l2levents:
            self.processfunctions.append(self.count2l2l)
        if config.countallleptonnumbers:
            self.processfunctions.append(self.countallleptonnumbers)
        if config.tree:
            self.anythingtofill = False
            self.processfunctions.append(self.filltree)

    def count(self, whattocount):
        return self.particlecounter.count(whattocount)

    def process(self):
        for prcs in self.processfunctions:
            prcs()

    def check(self):
        checks = self.miscellaneouschecks + [chk() for chk in self.checkfunctions]
        return "\n".join([chk for chk in checks if chk])

    def checkfirstline(self):
        results = []
        firstlinedata = self.firstline.split()
        try:
            Nparticles = int(firstlinedata[0])
            if Nparticles != len(list(self.particlecounter.elements())):
                results.append(str(len(list(self.particlecounter.elements()))) + " particles in the event, but " + str(Nparticles) + " recorded in the first line!" + str(self.linenumber))
        except ValueError:
            results.append("Number of particles is " + firstlinedata[0] + ", not an integer! " + str(self.linenumber))
        try:
            processid = int(firstlinedata[1])
        except ValueError:
            results.append("Process id is " + firstlinedata[1] + ", not an integer! " + str(self.linenumber))
        try:
            eventweight = float(firstlinedata[2])
        except ValueError:
            results.append("Event weight is " + firstlinedata[2] + ", not a number! " + str(self.linenumber))
        try:
            scale = float(firstlinedata[3])
        except ValueError:
            results.append("Scale is " + firstlinedata[3] + ", not a number! " + str(self.linenumber))
        try:
            scale = float(firstlinedata[4])
        except ValueError:
            results.append("alphaQED is " + firstlinedata[4] + ", not a number! " + str(self.linenumber))
        try:
            scale = float(firstlinedata[5])
        except ValueError:
            results.append("alphaQCD is " + firstlinedata[5] + ", not a number! " + str(self.linenumber))

    def checkstatus(self):
        results = []
        for p in self.particlelist:
            if p.status() not in [-1, 1, -2, 2, 3, -9]:
                results.append("Particle " + str(p) + " has unknown status " + str(p.status()) +  "! " + str(self.linenumber))

            if (p.status() == -1 or p.status() == -9) and any(p.mothers()):
                results.append("Particle " + str(p) + " with status " + str(p.status()) + " has mothers " + str(p.mothers()) + "! " + str(self.linenumber))
            if p.status() != -1 and p.status() != -9 and not any(p.mothers()):
                results.append("Particle " + str(p) + " with status " + str(p.status()) + " has no mothers! " + str(self.linenumber))

            if p.status() == 1 and p.kids():
                results.append("Particle " + str(p) + " with status 1 has kids " + str(p.kids()) + "! " + str(self.linenumber))
            if p.status() != 1 and not p.kids():
                results.append("Particle " + str(p) + " with status " + str(p.status()) + " has no kids! " + str(self.linenumber))

            if p.status() == -2 and p.lhemass() > 0:
                results.append("Particle " + str(p) + " with status -2 has m = " + str(p.lhemass()) + " > 0! " + str(self.linenumber))
            if p.status() != -2 and p.status() != 3 and p.lhemass() < 0:
                results.append("Particle " + str(p) + " with status " + str(p.status()) + " has m = " + str(p.lhemass()) + " < 0! " + str(self.linenumber))
        return "\n".join(results)

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
        for v in self.vertices.values():
            if v.momentumin() != v.momentumout():
                results.append("no momentum conservation! " + str(self.linenumber) + "\n" +
                               "mom momentum  = " + str(v.momentumin()) + str(v.particlesin()) + "\n" +
                               "kids momentum = " + str(v.momentumout()) + str(v.particlesout()))
        return "\n".join(results)

    def checkcharge(self):
        results = []
        for v in self.vertices.values():
            if v.chargein() != v.chargeout():
                results.append("no charge conservation! " + str(self.linenumber) + "\n" +
                               "mom charge  = " + str(v.chargein()) + str(v.particlesin()) + "\n" +
                               "kids charge = " + str(v.chargeout()) + str(v.particlesout()))
        return "\n".join(results)

    def checkcolor(self):
        results = []
        for p in self.particlelist:
            if not p.color() and ((p in globalvariables.globalvariables.quarks and p.id() > 0) or p in globalvariables.globalvariables.gluon):
                results.append(str(p) + " has no color! " + str(self.linenumber))
            if p.color() and not ((p in globalvariables.globalvariables.quarks and p.id() > 0) or p in globalvariables.globalvariables.gluon):
                results.append(str(p) + " has color " + str(p.color()) + "! " + str(self.linenumber))

            if not p.anticolor() and ((p in globalvariables.globalvariables.quarks and p.id() < 0) or p in globalvariables.globalvariables.gluon):
                results.append(str(p) + " has no anticolor! " + str(self.linenumber))
            if p.anticolor() and not ((p in globalvariables.globalvariables.quarks and p.id() < 0) or p in globalvariables.globalvariables.gluon):
                results.append(str(p) + " has anticolor " + str(p.anticolor()) + "! " + str(self.linenumber))

        for c in self.colors.values():
            if not c.check():
                results.append("color line " + str(c) + " doesn't make sense! " + str(self.linenumber) + "\n" +
                               "particles involved: " + str(c.particles.union(c.antiparticles)))
        return "\n".join(results)

    def count4l(self):
        if self.count(globalvariables.globalvariables.leptons) >= 4:
            globalvariables.globalvariables.any4l.increment()

    def count2l2l(self):
        leptons = [p for p in self.particlelist if p in globalvariables.globalvariables.leptons]
        if checkdebugoutput.count2l2l(leptons):
            globalvariables.globalvariables.any2l2l.increment()

    def countallleptonnumbers(self):
        for i in globalvariables.globalvariables.leptoncount:
            if self.count(globalvariables.globalvariables.leptons) == i:
                globalvariables.globalvariables.leptoncount[i].increment()
                return
        else:
            raise RuntimeError(str(self.count(globalvariables.globalvariables.leptons)) + "leptons in event! " + str(self.linenumber) + "\n" +
                               "increase the range of globalvariables.globalvariables.leptoncount")

    def higgs(self):
        higgslist = [p for p in self.particlelist if str(p) == "H" or str(p) == "Z'" or str(p) == "G"]
        if len(higgslist) == 0:
            raise IOError("No higgs in event! " + str(self.linenumber))
        if len(higgslist) > 1:
            raise IOError("Multiple higgs in event! " + str(self.linenumber))
        return higgslist[0]

    def higgsdecay(self, level = None):
        return particle.DecayType(self.higgs(), level).particles

    def higgsdecaytype(self, level = None):
        return particle.DecayType(self.higgs(), level)

    def checkhiggsdecay(self):
        if not self.higgs().kids():
            return ""
        for family in globalvariables.globalvariables.decayfamiliestoplevel:
            if self.higgs() in family:
                family.increment(self.higgs())
                return ""
        return ("unknown decay type! " + str(self.linenumber) + "\n" +
                "H -> " + str(self.higgsdecay()))

    def ishiggs(self):
        return len([p for p in self.particlelist if str(p) == "H" or str(p) == "Z'" or str(p) == "G"]) == 1


#VH
    def isVH(self):
        return bool(self.getVfromVH())
    def getVfromVH(self):
        immediateproduction = [p for p in self.particlelist if all(parent in self.incoming for parent in p.mothers())]
        counter = particle.ParticleCounter(immediateproduction)
        if counter.count(globalvariables.globalvariables.weakbosons) == 1 and counter.count(globalvariables.globalvariables.higgs) == 1:
            return [p for p in immediateproduction if p in globalvariables.globalvariables.weakbosons][0]
        else:
            return None

    def checkVdecay(self):
        V = self.getVfromVH()
        if V is None:
            return "Not VH event! " + str(self.linenumber)
        Vdecay = particle.DecayType(V)

        categories = None
        if V in globalvariables.globalvariables.W:
            categories = globalvariables.globalvariables.WH.increment(particle.DecayType(V))     #automatically increments the correct decay
        if V in globalvariables.globalvariables.Z:
            categories = globalvariables.globalvariables.ZH.increment(particle.DecayType(V))     #automatically increments the correct decay

        if categories is None:
            assert(0)                                        #Has to be ZH or WH

        if len(categories) == 1:
            return ("unknown V decay type! " + str(self.linenumber) + "\n" +
                    "V -> " + str(Vdecay))

        globalvariables.globalvariables.VH.increment()
        return ""

#conversion

    def boostall(self, xorvect, y = None, z = None):
        if y is None and z is not None or y is not None and z is None:
            raise TypeError
        if y is None and z is None:
            for p in self.particlelist:
                p.Boost(xorvect)
        else:
            for p in self.particlelist:
                p.Boost(x, y, z)

    def boosttocom(self, vect):
        boostvector = -vect.BoostVector()
        self.boostall(boostvector)

    def gotoframe(self, frame):
        self.boosttocom(frame.t)
        self.rotatetozx(frame.z, frame.x)

    def rotateall(self, angle, axis):
        for p in self.particlelist:
            p.Rotate(angle, axis)

    def rotatetozx(self, toz, tozx):
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
        self.rotateall(angle,axis)
        if tozx is not None:
            tozx.Rotate(angle,axis)

            angle2 = -tozx.Phi()
            axis2 = ROOT.TVector3(0,0,1)
            self.rotateall(angle2,axis2)

    def filltree(self):
        if self.anythingtofill:
            globalvariables.globalvariables.tree.Fill()

    def isZZ(self):
        return len(self.higgs().kids()) == 2 and all(kid in globalvariables.globalvariables.Z for kid in self.higgs().kids())

    def Z(self, which):
        if not self.isZZ():
            return None
        Zs = self.higgs().kids()
        assert(all(Z in globalvariables.globalvariables.Z for Z in Zs))
        Zs.sort(key = lambda Z: abs(Z.invmass() - Z.PDGmass()))
        return Zs[which - 1]

    def isWW(self):
        return len(self.higgs().kids()) == 2 and all(kid in globalvariables.globalvariables.W for kid in self.higgs().kids())

    def W(self, which):
        if not self.isWW():
            return None
        Ws = self.higgs().kids()
        assert(all(W in globalvariables.globalvariables.W for W in Ws))
        Ws.sort(key = lambda W: abs(W.invmass() - W.PDGmass()))
        return Ws[which - 1]

    def checkZZorWWassignment(self):
        if (self.higgs() not in globalvariables.globalvariables.decayZZ4l
        and self.higgs() not in globalvariables.globalvariables.decayZZ4q
        and self.higgs() not in globalvariables.globalvariables.decayZZ4nu
        and self.higgs() not in globalvariables.globalvariables.decayWW4q
        and self.higgs() not in globalvariables.globalvariables.decayWW2l2nu):
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

    def getZZ4langles(self):
        globalvariables.globalvariables.costheta1[0] = -999
        globalvariables.globalvariables.costheta2[0] = -999
        globalvariables.globalvariables.Phi[0] = -999

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
            if leptons[i] not in globalvariables.globalvariables.leptons:
                return
        self.boosttocom(Zs[1])
        globalvariables.globalvariables.costheta1[0] = -leptons[(1, 1)].Vect().Unit().Dot(Zs[2].Vect().Unit())
        self.boosttocom(Zs[2])
        globalvariables.globalvariables.costheta2[0] = -leptons[(2, 1)].Vect().Unit().Dot(Zs[1].Vect().Unit())

        self.boosttocom(self.higgs())
        normal1 = leptons[1, 1].Vect().Cross(leptons[1, -1].Vect()).Unit()
        normal2 = leptons[2, 1].Vect().Cross(leptons[2, -1].Vect()).Unit()
        globalvariables.globalvariables.Phi[0] = copysign(acos(-normal1.Dot(normal2)),Zs[1].Vect().Dot(normal1.Cross(normal2)))

        self.gotoframe(lab)
        self.anythingtofill = True

    def getZZmasses(self):
        globalvariables.globalvariables.mZ1[0] = -999
        globalvariables.globalvariables.mZ2[0] = -999
        globalvariables.globalvariables.mH[0] = -999
        Zs = {1: self.Z(1), 2: self.Z(2)}
        if Zs[1] is None or Zs[2] is None:
            return
        leptons = {}
        for Z in (1, 2):
            for sign in (1, -1):
                leptons[(Z, sign)] = [p for p in Zs[Z].kids() if p.id()*sign > 0][0]
        #sign is -charge
        for i in leptons:
            if leptons[i] not in globalvariables.globalvariables.leptons:
                return
        globalvariables.globalvariables.mZ1[0] = Zs[1].invmass()
        globalvariables.globalvariables.mZ2[0] = Zs[2].invmass()
        globalvariables.globalvariables.mH[0] = self.higgs().invmass()
        self.anythingtofill = True
