import particle
import particletype
import particlecategory

class event:
    def __init__(self, particlelist, linenumber):
        self.particlelist = particlelist
        self.linenumber = linenumber
        self.decaylist = [p for p in particlelist if p.status() == 2]

    def checkmass():
        result = ""
        for p in self.particlelist:
            lhemass = p.lhemass()
            if p.usemass()   == "physical":
                massshouldbe = p.physicalmass()
            elif p.usemass() == "invariant":
                massshouldbe = p.invmass()
            else:
                assert(0)
            if abs(p.invmass() - p.lhemass()) >= particle.masstolerance:
                result += ("Mass is wrong! " + str(self.self.linenumber) + "(" + str(p) + ")\n" +
                           p.usemass(True) + " mass = " + str(massshouldbe) + "\n" +
                           "lhe mass       = " + str(lhemass))
        return result

    def checkmomentum(self):
        for p in self.decaylist:
            mommomentum = p.momentum()
            kidsmomentum = sum([kid.momentum() for kid in p.kids()], particle.Momentum(0, 0, 0, 0))
            if mommomentum != kidsmomentum:
                result += ("no momentum conservation! " + str(self.linenumber) + "\n" +
                           "mom momentum  = " + str(mommomentum) + "("  + str(p) + ")\n" +
                           "kids momentum = " + str(kidsmomentum) + "(" + ", ".join([str(kid) for kid in p.kids()]) + ")")

    def checkcharge(self):
        for p in self.decaylist:
            momcharge = p.charge()
            kidscharge = sum([kid.charge() for kid in p.kids()])
            if momcharge != kidscharge:
                result += ("no charge conservation! " + str(self.linenumber) + "\n" +
                           "mom charge  = " + str(momcharge) + "("  + str(p) + ")\n" +
                           "kids charge = " + str(kidscharge) + "(" + ", ".join([str(kid) for kid in p.kids()]) + ")")

    def higgsdecaytype(self):
        decaylist = []

        higgs = [p for particle in particles if str(p) == "H"]
        if len(higgs) == 0:
            raise IOError("No higgs in event! " + str(self.linenumber))
        if len(higgs) > 1:
            raise IOError("Multiple higgs in event! " + str(self.linenumber))
        higgs = higgs[0]

        Hkids = higgs.kids()
        if len(Hkids) != 2:
            raise IOError("Unknown Higgs decay mode! " + str(self.linenumber))
        for kid in higgs.kids():
            if str(kid) == "gamma":
                decaylist += "gamma"
            else:
                grandkids = kid.kids()
                if all(p.ise() for p in grandkids):
                    decaylist += "2e"
                if all(p.ismu() for p in grandkids):
                    decaylist += "2mu"
                if all(p.istau() for p in grandkids):
                    decaylist += "2tau"
                if all(p.isneutrino() for p in grandkids):
                    decaylist += "2nu"
                if all(p.isquark() for p in grandkids):
                    decaylist += "2q"

