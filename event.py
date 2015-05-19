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

#############################
#        Event setup        #
#############################

    def __init__(self, linenumber, eventcounter, tree):
        self.linenumber = linenumber
        self.eventcounter = eventcounter
        self.tree = tree
        self.firstline = None
        self.particlelist = usefulstuff.printablelist([None])
        self.vertices = vertex.Vertices()
        self.colors = color.Colors()
        self.done = False
        self.momenta = []
        self.labframe = self.frame()

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
        self.particlelist.setmothers()
        self.particlelist.remove(None)
        self.particlecounter = particle.ParticleCounter(self.particlelist)

        self.decaylist = [p for p in self.particlelist if p.kids()]
        self.incoming = [p for p in self.particlelist if p.status() == -1]

        globalvariables.globalvariables.anyevent.increment(self.eventcounter)

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
        if config.makeZZmassestree:
            self.processfunctions.append(self.getZZmasses)
        if config.getHiggsMomentum:
            self.processfunctions.append(self.getHiggsMomentum)
        if config.getLeptonMomenta:
            self.processfunctions.append(self.getLeptonMomenta)
        if config.makeZZ4langlestree:
            self.processfunctions.append(self.getZZ4langles)

        if config.makeq2VBFtree:
            self.processfunctions.append(self.getq2VBF)
        if config.makeVBFanglestree:
            self.processfunctions.append(self.getVBFangles)
        if config.makeVBFjetvariablestree:
            self.processfunctions.append(self.getVBFjetvariables)

        if config.count4levents:
            self.processfunctions.append(self.countallleptonnumbers)
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
        checks = self.miscellaneouschecks + [chk() for chk in self.checkfunctions]
        return "\n".join([chk for chk in checks if chk])

##########################
#     Syntax checks      #
##########################

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

########################
#     Event counts     #
########################

    def count2l2l(self):
        leptons = [p for p in self.particlelist if p in globalvariables.globalvariables.leptons]
        if checkdebugoutput.count2l2l(leptons):
            globalvariables.globalvariables.any2l2l.increment(self.eventcounter)

    def countallleptonnumbers(self):
        if self.count(globalvariables.globalvariables.leptons) > max(globalvariables.globalvariables.leptoncount):
            raise RuntimeError(str(self.count(globalvariables.globalvariables.leptons)) + " leptons in event! " + str(self.linenumber) + "\n" +
                               "increase the range of globalvariables.globalvariables.leptoncount")
        for i in globalvariables.globalvariables.leptoncount:
            if not config.countallleptonnumbers and not (config.count4levents and i == 4):
                continue
            if self.count(globalvariables.globalvariables.leptons) >= i:
                globalvariables.globalvariables.leptoncount[i].increment(self.eventcounter)
                if self.count(globalvariables.globalvariables.emu) >= i:
                    globalvariables.globalvariables.emucount[i].increment(self.eventcounter)

#######################
#     Higgs decay     #
#######################

    def higgs(self, getmomentumifimplicit = False):
        higgslist = [p for p in self.particlelist if str(p) == "H" or str(p) == "Z'" or str(p) == "G"]
        if len(higgslist) == 0:
            if getmomentumifimplicit and self.higgsdecay():
                return sum((p.momentum() for p in self.higgsdecay()), momentum.Momentum(None, 0, 0, 0, 0))
            return None
        if len(higgslist) > 1:
            raise IOError("Multiple higgs in event! " + str(self.linenumber))
        return higgslist[0]

    def higgsdecay(self, level = None):
        decaytype = self.higgsdecaytype(level)
        if decaytype:
            return decaytype.particles
        return None

    def higgsdecaytype(self, level = None):
        if self.higgs():
            if self.higgs().kids():
                return particle.DecayType(self.higgs(), level)
            return None
        if config.allowimplicithiggs:
            if level is None:
                newlevel = None
            else:
                newlevel = level - 1
            return particle.DecayType([p for p in self.particlelist if (p in globalvariables.globalvariables.weakbosons
                                                                     or p in globalvariables.globalvariables.photon)
                                                                    and all(pp in self.incoming for pp in p.mothers())], newlevel)
        return None

    def checkhiggsdecay(self):
        if not self.higgsdecay():
            return ""
        for family in globalvariables.globalvariables.decayfamiliestoplevel:
            if self.higgsdecay(1) in family:
                family.increment(self.higgsdecay(1), self.eventcounter)
                return ""
        return ("unknown decay type! " + str(self.linenumber) + "\n" +
                "H --> " + str(self.higgsdecay()))

    def ishiggs(self):
        return len([p for p in self.particlelist if str(p) == "H" or str(p) == "Z'" or str(p) == "G"]) == 1

    def isZZ(self):
        if self.higgsdecay():
            return len(self.higgsdecay(1)) == 2 and all(kid in globalvariables.globalvariables.Z for kid in self.higgsdecay(1))
        return False

    def Z(self, which):
        if not self.isZZ():
            return None
        Zs = self.higgsdecay(1)
        assert(all(Z in globalvariables.globalvariables.Z for Z in Zs))
        Zs.sort(key = lambda Z: abs(Z.invmass() - Z.PDGmass()))
        return Zs[which - 1]

    def isWW(self):
        if self.higgsdecay():
            return len(self.higgsdecay(1)) == 2 and all(kid in globalvariables.globalvariables.W for kid in self.higgsdecay(1))
        return False

    def W(self, which):
        if not self.isWW():
            return None
        Ws = self.higgsdecay(1)
        assert(all(W in globalvariables.globalvariables.W for W in Ws))
        Ws.sort(key = lambda W: abs(W.invmass() - W.PDGmass()))
        return Ws[which - 1]

    def checkZZorWWassignment(self):
        if (self.higgsdecay() not in globalvariables.globalvariables.decayZZ4l
        and self.higgsdecay() not in globalvariables.globalvariables.decayZZ4q
        and self.higgsdecay() not in globalvariables.globalvariables.decayZZ4nu
        and self.higgsdecay() not in globalvariables.globalvariables.decayWW4q
        and self.higgsdecay() not in globalvariables.globalvariables.decayWW2l2nu):
            return ""
        assert(len(self.higgsdecay(1)) == 2)
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

########################
#          VH          #
########################

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
            categories = globalvariables.globalvariables.WH.increment(particle.DecayType(V), self.eventcounter)     #automatically increments the correct decay
        if V in globalvariables.globalvariables.Z:
            categories = globalvariables.globalvariables.ZH.increment(particle.DecayType(V), self.eventcounter)     #automatically increments the correct decay

        if categories is None:
            assert(0)                                        #Has to be ZH or WH

        if len(categories) == 1:
            return ("unknown V decay type! " + str(self.linenumber) + "\n" +
                    "V -> " + str(Vdecay))

        globalvariables.globalvariables.VH.increment(self.eventcounter)
        return ""

########################
#      Conversion      #
########################

    def boostall(self, xorvect, y = None, z = None):
        if y is None and z is not None or y is not None and z is None:
            raise TypeError
        elif y is None and z is None:
            args = [xorvect]
        else:
            args = [xorvect, y, z]

        for p in self.momenta:
            p.Boost(*args)

    def boosttocom(self, vect):
        boostvector = -vect.BoostVector()
        self.boostall(boostvector)

    def gotoframe(self, frame):
        self.boosttocom(frame.t)
        self.rotatetozx(frame.z, frame.x)

    def rotateall(self, angle, axis):
        for p in self.momenta:
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
            tozx.Rotate(angle, axis)
            angle2 = -tozx.Phi()
            axis2 = ROOT.TVector3(0,0,1)
            self.rotateall(angle2,axis2)

    def frame(self):
        return momentum.Frame(self)

    def filltree(self):
        if self.anythingtofill:
            self.tree.Fill(force = True, resetvalues = True)

###############################
#       ZZ4l conversion       #
###############################

    def getZZmasses(self):
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
        self.tree.EnsureBranch("mZ1", "D")
        self.tree.EnsureBranch("mZ2", "D")
        self.tree["mZ1"] = Zs[1].invmass()
        self.tree["mZ2"] = Zs[2].invmass()
        if self.higgs(True):
            self.tree.EnsureBranch("mH",  "D")
            self.tree["mH"] = self.higgs(True).invmass()
        self.anythingtofill = True

    def getHiggsMomentum(self):
        if not self.higgs(True):
            return
        self.gotoframe(self.labframe)
        self.tree.EnsureBranch("pTH", "D")
        self.tree.EnsureBranch("YH", "D")
        self.tree.EnsureBranch("etaH", "D")
        self.tree["pTH"] = self.higgs(True).Pt()
        self.tree["YH"] = self.higgs(True).Rapidity()
        self.tree["etaH"] = self.higgs(True).Eta()
        self.anythingtofill = True

    def getLeptonMomenta(self):
        #consistent with Ian's script
        flavortype = {
            (11, 11): 0,
            (13, 13): 1,
            (15, 15): 2,
            (11, 13): 3,
            (11, 15): 4,
            (13, 15): 5,
            (13, 11): 6,
            (15, 11): 7,
            (15, 13): 8,
        }

        self.gotoframe(self.labframe)
        Zs = {1: self.Z(1), 2: self.Z(2)}
        leptons = {}
        for Z in (1, 2):
            if Zs[Z] is None:
                return
            for sign in (1, -1):
                leptons[(Z, sign)] = [p for p in Zs[Z].kids() if p.id()*sign > 0][0]
        #sign is -charge
        for i in leptons:
            if leptons[i] not in globalvariables.globalvariables.leptons:
                return
        leptonstring = {(1, 1): "l1m", (1, -1): "l1p", (2, 1): "l2m", (2, -1): "l2p"}

        for i in leptons:
            self.tree.EnsureBranch(leptonstring[i] + "_phi", "D")
            self.tree.EnsureBranch(leptonstring[i] + "_pT", "D")
            self.tree.EnsureBranch(leptonstring[i] + "_eta", "D")
            self.tree[leptonstring[i] + "_phi"] = leptons[i].Phi()
            self.tree[leptonstring[i] + "_pT"] = leptons[i].Pt()
            self.tree[leptonstring[i] + "_eta"] = leptons[i].Eta()

        self.tree.EnsureBranch("flavortype", "I")
        self.tree["flavortype"] = flavortype[(leptons[(1, 1)].id(), leptons[(2, 1)].id())]
        self.anythingtofill = True

    def getZZ4langles(self):
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

        self.tree.EnsureBranch("costhetastar_ZZ4l", "D")
        self.tree.EnsureBranch("costheta1_ZZ4l",    "D")
        self.tree.EnsureBranch("costheta2_ZZ4l",    "D")
        self.tree.EnsureBranch("Phi_ZZ4l",          "D")
        self.tree.EnsureBranch("Phi1_ZZ4l",         "D")
        self.tree.EnsureBranch("costhetastar_ZZ4l_zhat", "D")
        self.tree.EnsureBranch("Phi1_ZZ4l_zhat",         "D")
        self.tree.EnsureBranch("costhetastar_ZZ4l_parton", "D")
        self.tree.EnsureBranch("Phi1_ZZ4l_parton",         "D")

        self.boosttocom(Zs[1])
        self.tree["costheta1_ZZ4l"] = -leptons[(1, 1)].Vect().Unit().Dot(Zs[2].Vect().Unit())
        self.boosttocom(Zs[2])
        self.tree["costheta2_ZZ4l"] = -leptons[(2, 1)].Vect().Unit().Dot(Zs[1].Vect().Unit())

        self.gotoframe(self.labframe)
        self.boosttocom(self.higgs(True))
        normal1 = leptons[1, 1].Vect().Cross(leptons[1, -1].Vect()).Unit()
        normal2 = leptons[2, 1].Vect().Cross(leptons[2, -1].Vect()).Unit()
        self.tree["Phi_ZZ4l"] = copysign(acos(-normal1.Dot(normal2)), Zs[1].Vect().Dot(normal1.Cross(normal2)))

        #I don't fully understand this beam axis definition, since we're boosted to the Higgs frame
        #in a way that doesn't preserve the z direction.  I would have done it using 2 successive boosts,
        #first to boost away the pT of the Higgs and then the pz.  This way the z direction is preserved.
        #(or, equivalently, use self.labframe.z.Vect().Unit(), since the labframe's unit vectors get boosted
        # in the same way as the other vectors).
        #Alternatively, use the momentum of the partons (which is (0,0,1,1) in the lab frame
        # since we only care about the direction, not the magnitude)

        #However, this way is compatible with all the older scripts that I see.
        #For ggH with no jets it's irrelevant, since the Higgs has pT=0 anyway.  However, for VBF, HJJ, VH, ...
        #it would make a difference.
        beamaxis = ROOT.TVector3(0,0,1)
        self.tree["costhetastar_ZZ4l"] = Zs[1].Vect().Unit().Dot(beamaxis)
        normal3 = beamaxis.Cross(Zs[1].Vect()).Unit()
        self.tree["Phi1_ZZ4l"] = copysign(acos(normal1.Dot(normal3)), Zs[1].Vect().Dot(normal1.Cross(normal3)))

        beamaxis = self.labframe.z.Vect().Unit()
        self.tree["costhetastar_ZZ4l_zhat"] = Zs[1].Vect().Unit().Dot(beamaxis)
        normal3 = beamaxis.Cross(Zs[1].Vect()).Unit()
        self.tree["Phi1_ZZ4l_zhat"] = copysign(acos(normal1.Dot(normal3)), Zs[1].Vect().Dot(normal1.Cross(normal3)))

        beamaxis = (self.labframe.z + self.labframe.t).Vect().Unit()
        self.tree["costhetastar_ZZ4l_parton"] = Zs[1].Vect().Unit().Dot(beamaxis)
        normal3 = beamaxis.Cross(Zs[1].Vect()).Unit()
        self.tree["Phi1_ZZ4l_parton"] = copysign(acos(normal1.Dot(normal3)), Zs[1].Vect().Dot(normal1.Cross(normal3)))


        self.gotoframe(self.labframe)
        self.anythingtofill = True

###################
#       VBF       #
###################

    def getproductionjets(self):
        return [p for p in self.particlelist if all(parent in self.incoming for parent in p.mothers()) \
                    and p in globalvariables.globalvariables.jets]

    def VBFjet(self, i, usepzorpT):
        jets = self.getproductionjets()
        if len(jets) > 2:
            raise NotImplementedError("VBF not implemented with >2 jets")
        if len(jets) < 2:
            return None
        if usepzorpT == "pz":
            jets.sort(key = lambda j: j.Pz(), reverse = True)
        elif usepzorpT == "pT":
            jets.sort(key = lambda j: j.Pt(), reverse = True)
        else:
            raise ValueError('You need to indicate whether jets should be sorted by pz or pT')
        return jets[i-1]

    def incomingparton(self, i, uselhepartons = False):
        if uselhepartons:
            partons = self.incoming
            if len(partons) != 2:
                raise NotImplementedError("There should be exactly 2 incoming partons")
            partons.sort(key = lambda p: p.Pz(), reverse = True)
            return partons[i-1]
        else:
            bkpframe = self.frame()
            jet1 = self.VBFjet(1, "pz")
            jet2 = self.VBFjet(2, "pz")
            if jet1 is None or jet2 is None:
                return None
            HJJ = self.higgs(True).momentum() + jet1.momentum() + jet2.momentum()
            HJJ_T = momentum.Momentum(self, HJJ.Px(), HJJ.Py(), 0, HJJ.E())
            self.boosttocom(HJJ_T)
            self.boosttocom(HJJ)     #sequential boosts to preserve the z direction
            pzsign = {1: 1, 2: -1}
            parton = momentum.Momentum(self, 0, 0, pzsign[i]*HJJ.E()/2, HJJ.E()/2)
            self.gotoframe(bkpframe)
            return parton

    def VBFV(self, i, uselhepartons = False):
        try:
            return self.VBFjet(i, "pz").momentum() - self.incomingparton(i, uselhepartons).momentum()
        except AttributeError:   #jet or parton (actually should be both or neither) is None
            return None

    def getq2VBF(self, uselhepartons = False):
        if uselhepartons:
            appendstring = "_lhe"
        else:
            appendstring = ""
        q2V1 = "q2V1" + appendstring
        q2V2 = "q2V2" + appendstring

        V1 = self.VBFV(1, uselhepartons)
        V2 = self.VBFV(2, uselhepartons)
        if V1 is None or V2 is None:
            return

        self.tree.EnsureBranch(q2V1, "D")
        self.tree.EnsureBranch(q2V2, "D")
        self.tree[q2V1] = V1.M2()
        self.tree[q2V2] = V2.M2()

    def getVBFangles(self, uselhepartons = True):
        try:
            jet1 = self.VBFjet(1, "pz").momentum()
            jet2 = self.VBFjet(2, "pz").momentum()
            V1 = self.VBFV(1, uselhepartons).momentum()
            V2 = self.VBFV(2, uselhepartons).momentum()
            P1 = self.incomingparton(1, uselhepartons).momentum()
            P2 = self.incomingparton(2, uselhepartons).momentum()
        except AttributeError:
            return

        self.boosttocom(self.higgs(True))

        self.tree.EnsureBranch("costheta1_VBF", "D")
        self.tree.EnsureBranch("costheta2_VBF", "D")
        self.tree.EnsureBranch("Phi_VBF",       "D")

        self.tree["costheta1_VBF"] = -V1.Vect().Dot(jet1.Vect())/jet1.Vect().Mag()/V1.Vect().Mag()
        self.tree["costheta2_VBF"] = -V2.Vect().Dot(jet2.Vect())/jet2.Vect().Mag()/V2.Vect().Mag()
        tmp1 = P1.Vect().Cross(jet1.Vect()).Unit()
        tmp2 = P2.Vect().Cross(jet2.Vect()).Unit()
        cosPhi = tmp1.Dot(tmp2)
        sgnPhi = tmp1.Cross(tmp2).Dot(V1.Vect())
        self.tree["Phi_VBF"] = copysign(acos(cosPhi), sgnPhi)

        if config.makeVBFdecayanglestree and self.isZZ():
            Z1 = self.Z(1)
            self.tree.EnsureBranch("costhetastar_VBF", "D")
            self.tree.EnsureBranch("Phi1_VBF",         "D")
            self.tree["costhetastar_VBF"] = -V1.Vect().Dot(Z1.Vect())/V1.Vect().Mag()/Z1.Vect().Mag()
            tmp3 = V1.Vect().Cross(Z1.Vect()).Unit()
            cosPhi1 = -tmp1.Dot(tmp3)
            sgnPhi1 = tmp1.Dot(Z1.Vect())
            self.tree["Phi1_VBF"] = copysign(acos(cosPhi1), sgnPhi1)

    def getVBFjetvariables(self):
        self.gotoframe(self.labframe)
        try:
            jet1 = self.VBFjet(1, "pT").momentum()
            jet2 = self.VBFjet(2, "pT").momentum()
        except AttributeError:
            return
        self.tree.EnsureBranch("mJJ_VBF",  "D")
        self.tree.EnsureBranch("dEta_VBF", "D")
        self.tree.EnsureBranch("dPhi_VBF", "D")
        self.tree.EnsureBranch("dR_VBF",   "D")
        self.tree["mJJ_VBF"] = (jet1+jet2).M()
        self.tree["dEta_VBF"] = jet1.Eta() - jet2.Eta()
        self.tree["dPhi_VBF"] = jet1.DeltaPhi(jet2)
        self.tree["dR_VBF"] = jet1.DeltaR(jet2)
