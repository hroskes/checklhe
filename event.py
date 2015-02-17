import particle
import particletype
import particlecategory
import globalvariables

class Event:
    def __init__(self, particlelist, linenumber):
        self.particlelist = [p for p in particlelist if p is not None]
        self.particlecounter = particle.ParticleCounter(particlelist)
        self.linenumber = linenumber
        self.decaylist = [p for p in self.particlelist if p.status() == 2]

        globalvariables.nevents += 1
        if self.count(globalvariables.leptons) >= 4:
            globalvariables.n4l += 1

    def count(self, whattocount):
        return self.particlecounter.count(whattocount)

    def check(self):
        return "\n".join([self.checkmass(), self.checkmomentum(), self.checkcharge(), self.checkhiggsdecay()])
        
    def checkmass(self):
        result = ""
        for p in self.particlelist:
            if abs(p.usemass() - p.lhemass()) >= globalvariables.masstolerance:
                result += ("Mass is wrong! " + str(self.self.linenumber) + "(" + str(p) + ")\n" +
                           "invariant mass = " + str(p.usemass()) + "\n" +
                           "lhe mass       = " + str(p.lhemass()))
        return result

    def checkmomentum(self):
        result = ""
        for p in self.decaylist:
            mommomentum = p.momentum()
            kidsmomentum = sum([kid.momentum() for kid in p.kids()], particle.Momentum(0, 0, 0, 0))
            if mommomentum != kidsmomentum:
                result += ("no momentum conservation! " + str(self.linenumber) + "\n" +
                           "mom momentum  = " + str(mommomentum) + "("  + str(p) + ")\n" +
                           "kids momentum = " + str(kidsmomentum) + "(" + ", ".join([str(kid) for kid in p.kids()]) + ")")
        return result

    def checkcharge(self):
        result = ""
        for p in self.decaylist:
            momcharge = p.charge()
            kidscharge = sum([kid.charge() for kid in p.kids()])
            if momcharge != kidscharge:
                result += ("no charge conservation! " + str(self.linenumber) + "\n" +
                           "mom charge  = " + str(momcharge) + "("  + str(p) + ")\n" +
                           "kids charge = " + str(kidscharge) + "(" + ", ".join([str(kid) for kid in p.kids()]) + ")")
        return result

    def higgsdecaytype(self):
        decaylist = []

        higgs = [p for p in self.particlelist if str(p) == "H"]
        if len(higgs) == 0:
            raise IOError("No higgs in event! " + str(self.linenumber))
        if len(higgs) > 1:
            raise IOError("Multiple higgs in event! " + str(self.linenumber))
        higgs = higgs[0]

        return particle.DecayType(higgs)

    def checkhiggsdecay(self):
        higgsdecay = self.higgsdecaytype()
        for family in globalvariables.decayfamilies4l:
            if higgsdecay in family:
                globalvariables.decaycounter[family] += 1
        for family in globalvariables.decayfamilies:
            if higgsdecay in family:
                globalvariables.decaycounter[family] += 1
                return ""
        return ("unknown decay type! " + str(self.linenumber) + "\n" +
                "H -> " + str(higgsdecay))

