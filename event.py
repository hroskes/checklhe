import particle
import particletype
import particlecategory
import globalvariables
import config

class Event:
    def __init__(self, particlelist, linenumber):
        self.particlelist = [p for p in particlelist if p is not None]
        self.particlecounter = particle.ParticleCounter(particlelist)
        self.linenumber = linenumber
        self.decaylist = [p for p in self.particlelist if p.status() == 2]

        globalvariables.eventcounter[globalvariables.anyevent] += 1
        if config.count4levents and self.count(globalvariables.leptons) >= 4:
            globalvariables.eventcounter[globalvariables.any4l] += 1

        self.checkfunctions = [self.checkmass, self.checkmomentum, self.checkcharge, self.checkhiggsdecay]

    def count(self, whattocount):
        return self.particlecounter.count(whattocount)

    def check(self):
        checks = [chk() for chk in self.checkfunctions]
        return "\n".join([chk for chk in checks if chk])
        
    def checkmass(self):
        if not config.checkmass:
            return ""
        results = []
        for p in self.particlelist:
            if abs(p.usemass() - p.lhemass()) >= globalvariables.masstolerance:
                results.append("Mass is wrong! " + str(self.linenumber) + "(" + str(p) + ")\n" +
                               "invariant mass = " + str(p.usemass()) + "\n" +
                               "lhe mass       = " + str(p.lhemass()))
        return "\n".join(results)

    def checkmomentum(self):
        if not config.checkmomentum:
            return ""
        results = []
        for p in self.decaylist:
            mommomentum = p.momentum()
            kidsmomentum = sum([kid.momentum() for kid in p.kids()], particle.Momentum(0, 0, 0, 0))
            if mommomentum != kidsmomentum:
                results.append("no momentum conservation! " + str(self.linenumber) + "\n" +
                               "mom momentum  = " + str(mommomentum) + "("  + str(p) + ")\n" +
                               "kids momentum = " + str(kidsmomentum) + "(" + ", ".join([str(kid) for kid in p.kids()]) + ")")
        return "\n".join(results)

    def checkcharge(self):
        if not config.checkcharge:
            return ""
        results = []
        for p in self.decaylist:
            momcharge = p.charge()
            kidscharge = sum([kid.charge() for kid in p.kids()])
            if momcharge != kidscharge:
                results.append("no charge conservation! " + str(self.linenumber) + "\n" +
                               "mom charge  = " + str(momcharge) + "("  + str(p) + ")\n" +
                               "kids charge = " + str(kidscharge) + "(" + ", ".join([str(kid) for kid in p.kids()]) + ")")
        return "\n".join(results)

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
        if not config.countZZdecaytype:
            return ""
        higgsdecay = self.higgsdecaytype()
        for family in globalvariables.decaysubcategories:
            if higgsdecay in family:
                globalvariables.eventcounter[family] += 1
        for family in globalvariables.decayfamiliestoplevel:
            if higgsdecay in family:
                globalvariables.eventcounter[family] += 1
                return ""
        return ("unknown decay type! " + str(self.linenumber) + "\n" +
                "H -> " + str(higgsdecay))
