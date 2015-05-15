import particlecategory
import particle
import config
import collections
import cPickle

eventcounter = collections.Counter()

startedinit = False
finishedinit = False

class GlobalVariablesMinimal:
    #for stuff that's needed before GlobalVariables is inited
    #I'm aware this is ugly
    def __init__(self):
        class ParticleCategory:
            def __init__(self, particles):
                self.particles = particles
            def ids(self):
                return self.particles

        self.neutralbosons = ParticleCategory([21, 22, 23, 25, 32, 39])

class GlobalVariables:
    def __init__(self):
        self.startedinit = False
        self.finishedinit = False

    #Not __init__, I want the object to exist even before the variables are assigned
    def init(self):
        if self.startedinit:
            return
        self.startedinit = True

        #Particle categories
        self.neutralbosons = particlecategory.ParticleCategory([21, 22, 23, 25, 32, 39], Csymmetric = False)

        self.electrons = particlecategory.ParticleCategory([11])
        self.muons = particlecategory.ParticleCategory([13])
        self.taus = particlecategory.ParticleCategory([15])
        self.leptons = self.electrons.union(self.muons).union(self.taus)

        self.neutrinos = particlecategory.ParticleCategory([12, 14, 16])

        self.down    = particlecategory.ParticleCategory([1])
        self.up      = particlecategory.ParticleCategory([2])
        self.strange = particlecategory.ParticleCategory([3])
        self.charm   = particlecategory.ParticleCategory([4])
        self.bottom  = particlecategory.ParticleCategory([5])
        self.top     = particlecategory.ParticleCategory([6])
        self.uptypequarks = self.up.union(self.charm).union(self.top)
        self.downtypequarks = self.down.union(self.strange).union(self.bottom)
        self.quarks = self.uptypequarks.union(self.downtypequarks)

        self.gluon = particlecategory.ParticleCategory([21])
        self.photon = particlecategory.ParticleCategory([22])
        self.weakbosons = particlecategory.ParticleCategory([23, 24])
        self.Z = particlecategory.ParticleCategory([23])
        self.W = particlecategory.ParticleCategory([24])
        self.higgs = particlecategory.ParticleCategory([25, 32, 39])

        self.jets = self.quarks.difference(self.top).union(self.gluon)
        print "initialized particle categories"

        #4l decays by flavor
        self.decayZZ4e = particle.DecayFamily([[11, 11, -11, -11]], name = "H --> ZZ --> 4e")
        self.decayZZ4mu = particle.DecayFamily([[13, 13, -13, -13]], name = "H --> ZZ --> 4mu")
        self.decayZZ4tau = particle.DecayFamily([[15, 15, -15, -15]], name = "H --> ZZ --> 4tau")
        self.decayZZ2e2mu = particle.DecayFamily([[11, 13, -11, -13]], name = "H --> ZZ --> 2e2mu")
        self.decayZZ2e2tau = particle.DecayFamily([[11, 15, -11, -15]], name = "H --> ZZ --> 2e2tau")
        self.decayZZ2mu2tau = particle.DecayFamily([[13, 15, -13, -15]], name = "H --> ZZ --> 2mu2tau")
        self.decayfamiliesZZ4l = [self.decayZZ4e, self.decayZZ4mu, self.decayZZ4tau, self.decayZZ2e2mu, self.decayZZ2e2tau, self.decayZZ2mu2tau]

        #2l2q decays by flavor
        self.decayZZ2e2q = particle.DecayFamily([[self.electrons, self.electrons, self.quarks, self.quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 2e2q")
        self.decayZZ2mu2q = particle.DecayFamily([[self.muons, self.muons, self.quarks, self.quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 2mu2q")
        self.decayZZ2tau2q = particle.DecayFamily([[self.taus, self.taus, self.quarks, self.quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 2tau2q")
        self.decayfamiliesZZ2l2q = [self.decayZZ2e2q, self.decayZZ2mu2q, self.decayZZ2tau2q]

        #2l2nu decays by flavor
        self.decayZZ2e2nu = particle.DecayFamily([[self.electrons, self.electrons, self.neutrinos, self.neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 2e2nu")
        self.decayZZ2mu2nu = particle.DecayFamily([[self.muons, self.muons, self.neutrinos, self.neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 2mu2nu")
        self.decayZZ2tau2nu = particle.DecayFamily([[self.taus, self.taus, self.neutrinos, self.neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 2tau2nu")
        self.decayfamiliesZZ2l2nu = [self.decayZZ2e2nu, self.decayZZ2mu2nu, self.decayZZ2tau2nu]
        self.decayWW2e2nu = particle.DecayFamily([[self.electrons, self.electrons, self.neutrinos, self.neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW --> 2e2nu")
        self.decayWW2mu2nu = particle.DecayFamily([[self.muons, self.muons, self.neutrinos, self.neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW --> 2mu2nu")
        self.decayWW2tau2nu = particle.DecayFamily([[self.taus, self.taus, self.neutrinos, self.neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW --> 2tau2nu")
        self.decayWWemu2nu = particle.DecayFamily([[self.electrons, self.muons, self.neutrinos, self.neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW -->emu2nu")
        self.decayWWetau2nu = particle.DecayFamily([[self.electrons, self.taus, self.neutrinos, self.neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW -->etau2nu")
        self.decayWWmutau2nu = particle.DecayFamily([[self.muons, self.taus, self.neutrinos, self.neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW -->mutau2nu")
        self.decayfamiliesWW2l2nu = [self.decayWW2e2nu, self.decayWW2mu2nu, self.decayWW2tau2nu, self.decayWWemu2nu, self.decayWWetau2nu, self.decayWWmutau2nu]

        #lnu2q decays by flavor
        self.decayWWlplusnu2q = particle.DecayFamily([[[-11], self.neutrinos, self.quarks, self.quarks], [[-13], self.neutrinos, self.quarks, self.quarks], [[-15], self.neutrinos, self.quarks, self.quarks]],
                                                                                 charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW --> l+nu2q", Csymmetric = False)
        self.decayWWlminusnu2q = particle.DecayFamily([[[+11], self.neutrinos, self.quarks, self.quarks], [[+13], self.neutrinos, self.quarks, self.quarks], [[+15], self.neutrinos, self.quarks, self.quarks]],
                                                                                 charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW --> l-nu2q", Csymmetric = False)
        self.decayfamiliesWWlnu2q = []
        self.decayWWenu2q = particle.DecayFamily([[self.electrons, self.neutrinos, self.quarks, self.quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW --> enu2q")
        self.decayWWmunu2q = particle.DecayFamily([[self.muons, self.neutrinos, self.quarks, self.quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW --> munu2q")
        self.decayWWtaunu2q = particle.DecayFamily([[self.taus, self.neutrinos, self.quarks, self.quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW --> taunu2q")
        self.decayfamiliesWWlnu2q = [self.decayWWlplusnu2q, self.decayWWlminusnu2q, self.decayWWenu2q, self.decayWWmunu2q, self.decayWWtaunu2q]

        #top level decay categories
        self.decayZZ4l = particle.DecayFamily([[self.leptons, self.leptons, self.leptons, self.leptons]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 4l",
                                       subcategories = self.decayfamiliesZZ4l)
        self.decayZZ2l2q = particle.DecayFamily([[self.quarks, self.quarks, self.leptons, self.leptons]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 2l2q",
                                         subcategories = self.decayfamiliesZZ2l2q)
        self.decayZZ2l2nu = particle.DecayFamily([[self.neutrinos, self.neutrinos, self.leptons, self.leptons]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 2l2nu",
                                          subcategories = self.decayfamiliesZZ2l2nu)
        self.decayWW2l2nu = particle.DecayFamily([[self.neutrinos, self.neutrinos, self.leptons, self.leptons]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW --> 2l2nu",
                                          subcategories = self.decayfamiliesWW2l2nu)
        self.decayWWlnu2q = particle.DecayFamily([[self.leptons, self.neutrinos, self.quarks, self.quarks]], charge = 0, leptonnumber = (0,0,0), baryonnumber = 0, name = "H --> WW -->lnu2q",
                                          subcategories = self.decayfamiliesWWlnu2q)
        self.decayZZ2q2nu = particle.DecayFamily([[self.quarks, self.quarks, self.neutrinos, self.neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 2q2nu")
        self.decayZZ4q = particle.DecayFamily([[self.quarks, self.quarks, self.quarks, self.quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 4q")
        self.decayWW4q = particle.DecayFamily([[self.quarks, self.quarks, self.quarks, self.quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW --> 4q")
        self.decayZZ4nu = particle.DecayFamily([[self.neutrinos, self.neutrinos, self.neutrinos, self.neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 4nu")

        #Higgs decay families
        self.HZZ = particle.DecayFamily([[self.Z, self.Z]], name = "H --> ZZ", subcategories = [self.decayZZ4l, self.decayZZ2l2q, self.decayZZ2l2nu, self.decayZZ4q, self.decayZZ4nu, self.decayZZ2q2nu])
        self.HWW = particle.DecayFamily([[self.W, self.W]], charge = 0, name = "H --> WW", subcategories = [self.decayWW2l2nu, self.decayWW4q, self.decayWWlnu2q])
        self.decayfamiliestoplevel = [self.HZZ, self.HWW]

        print "initialized Higgs decay"

        ################
        #      VH      #
        ################

        #Z 2l decay families
        self.Zdecay2e = particle.DecayFamily([[self.electrons, self.electrons]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "Z --> 2e")
        self.Zdecay2mu = particle.DecayFamily([[self.muons, self.muons]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "Z --> 2mu")
        self.Zdecay2tau = particle.DecayFamily([[self.taus, self.taus]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "Z --> 2tau")
        self.Zdecayfamilies2l = [self.Zdecay2e, self.Zdecay2mu, self.Zdecay2tau]

        #Wminus lnu decay families
        self.Wminusdecayenu = particle.DecayFamily([[self.electrons, self.neutrinos]], charge = -1, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "W- --> enu")
        self.Wminusdecaymunu = particle.DecayFamily([[self.muons, self.neutrinos]], charge = -1, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "W- --> munu")
        self.Wminusdecaytaunu = particle.DecayFamily([[self.taus, self.neutrinos]], charge = -1, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "W- --> taunu")
        self.Wminusdecayfamilieslnu = [self.Wminusdecayenu, self.Wminusdecaymunu, self.Wminusdecaytaunu]

        #Wplus lnu decay families
        self.Wplusdecayenu = particle.DecayFamily([[self.electrons, self.neutrinos]], charge = 1, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "W+ --> enu")
        self.Wplusdecaymunu = particle.DecayFamily([[self.muons, self.neutrinos]], charge = 1, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "W+ --> munu")
        self.Wplusdecaytaunu = particle.DecayFamily([[self.taus, self.neutrinos]], charge = 1, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "W+ --> taunu")
        self.Wplusdecayfamilieslnu = [self.Wplusdecayenu, self.Wplusdecaymunu, self.Wplusdecaytaunu]

        #Wminus qqb' decay families
        self.Wminusdecayubard = particle.DecayFamily([[self.up, self.down]], charge = -1, name = "W- --> ubar d")
        self.Wminusdecayubars = particle.DecayFamily([[self.up, self.strange]], charge = -1, name = "W- --> ubar s")
        self.Wminusdecayubarb = particle.DecayFamily([[self.up, self.bottom]], charge = -1, name = "W- --> ubar b")
        self.Wminusdecaycbard = particle.DecayFamily([[self.charm, self.down]], charge = -1, name = "W- --> cbar d")
        self.Wminusdecaycbars = particle.DecayFamily([[self.charm, self.strange]], charge = -1, name = "W- --> cbar s")
        self.Wminusdecaycbarb = particle.DecayFamily([[self.charm, self.bottom]], charge = -1, name = "W- --> cbar b")
        self.Wminusdecaytbard = particle.DecayFamily([[self.top, self.down]], charge = -1, name = "W- --> tbar d")
        self.Wminusdecaytbars = particle.DecayFamily([[self.top, self.strange]], charge = -1, name = "W- --> tbar s")
        self.Wminusdecaytbarb = particle.DecayFamily([[self.top, self.bottom]], charge = -1, name = "W- --> tbar b")
        self.Wminusdecayfamilies2q = [self.Wminusdecayubard, self.Wminusdecayubars, self.Wminusdecayubarb, self.Wminusdecaycbard, self.Wminusdecaycbars, self.Wminusdecaycbarb, self.Wminusdecaytbard, self.Wminusdecaytbars, self.Wminusdecaytbarb]

        #Wplus qqb' decay families
        self.Wplusdecayudbar = particle.DecayFamily([[self.up, self.down]], charge = 1, name = "W+ --> u dbar")
        self.Wplusdecayusbar = particle.DecayFamily([[self.up, self.strange]], charge = 1, name = "W+ --> u sbar")
        self.Wplusdecayubbar = particle.DecayFamily([[self.up, self.bottom]], charge = 1, name = "W+ --> u bbar")
        self.Wplusdecaycdbar = particle.DecayFamily([[self.charm, self.down]], charge = 1, name = "W+ --> c dbar")
        self.Wplusdecaycsbar = particle.DecayFamily([[self.charm, self.strange]], charge = 1, name = "W+ --> c sbar")
        self.Wplusdecaycbbar = particle.DecayFamily([[self.charm, self.bottom]], charge = 1, name = "W+ --> c bbar")
        self.Wplusdecaytdbar = particle.DecayFamily([[self.top, self.down]], charge = 1, name = "W+ --> t dbar")
        self.Wplusdecaytsbar = particle.DecayFamily([[self.top, self.strange]], charge = 1, name = "W+ --> t sbar")
        self.Wplusdecaytbbar = particle.DecayFamily([[self.top, self.bottom]], charge = 1, name = "W+ --> t bbar")
        self.Wplusdecayfamilies2q = [self.Wplusdecayudbar, self.Wplusdecayusbar, self.Wplusdecayubbar, self.Wplusdecaycdbar, self.Wplusdecaycsbar, self.Wplusdecaycbbar, self.Wplusdecaytdbar, self.Wplusdecaytsbar, self.Wplusdecaytbbar]

        #VH decay families
        self.Zdecay2l = particle.DecayFamily([[self.leptons, self.leptons]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "Z --> 2l",
                                        subcategories = self.Zdecayfamilies2l)
        self.Zdecay2q = particle.DecayFamily([[self.quarks, self.quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "Z --> 2q")
        self.Zdecay2nu = particle.DecayFamily([[self.neutrinos, self.neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "Z --> 2nu")
        self.Wminusdecaylnu = particle.DecayFamily([[self.leptons, self.neutrinos]], charge = -1, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "W- --> lnu",
                                              subcategories = self.Wminusdecayfamilieslnu)
        self.Wplusdecaylnu = particle.DecayFamily([[self.leptons, self.neutrinos]], charge = +1, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "W+ --> lnu",
                                             subcategories = self.Wplusdecayfamilieslnu)
        self.Wminusdecay2q = particle.DecayFamily([[self.quarks, self.quarks]], charge = -1, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "W- --> 2q",
                                             subcategories = self.Wminusdecayfamilies2q)
        self.Wplusdecay2q = particle.DecayFamily([[self.quarks, self.quarks]], charge = 1, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "W+ --> 2q",
                                             subcategories = self.Wplusdecayfamilies2q)

        self.Zdecaycategories = [self.Zdecay2l, self.Zdecay2q, self.Zdecay2nu]
        self.ZH = particle.DecayFamily([], name = "ZH", subcategories = self.Zdecaycategories)
        self.Wdecaycategories = [self.Wminusdecaylnu, self.Wplusdecaylnu, self.Wminusdecay2q, self.Wplusdecay2q]
        self.WH = particle.DecayFamily([], name = "WH", subcategories = self.Wdecaycategories)

        self.VH = particle.EventCount("VH", [self.ZH, self.WH])

        print "initialized VH decay"

        #big categories
        self.leptoncount = {}
        for i in range(10):
            self.leptoncount[i] = particle.EventCount("exactly" + str(i) + "l", [])

        self.any2l2lsubcats = []
        if config.counthiggsdecaytype:
            self.any2l2lsubcats.append(self.decayZZ4l)
        self.any2l2l = particle.EventCount("2l2l", self.any2l2lsubcats)
        self.any4l = particle.EventCount("4l", [self.any2l2l, self.leptoncount[4]])

        self.anyeventsubcats = [(self.leptoncount[i] if i != 4 else self.any4l) for i in self.leptoncount]
        if config.counthiggsdecaytype:
            self.anyeventsubcats += [self.HZZ, self.HWW]
        if config.countVHdecaytype:
            self.anyeventsubcats += [self.VH]
        self.anyevent = particle.EventCount("total", self.anyeventsubcats)

        config.init()
        self.finishedinit = True



def init():
    global globalvariables, startedinit, finishedinit
    if startedinit:
        return
    startedinit = True

    try:
        with open("globalvariables.pkl", "rb") as f:
            globalvariables = GlobalVariablesMinimal()
            globalvariables = cPickle.load(f)
    except (IOError, cPickle.UnpicklingError):
        globalvariables = GlobalVariables()
        globalvariables.init()
        #cPickle.dump(globalvariables, open("globalvariables.pkl", "wb"))

    if not config.counthiggsdecaytype:
        globalvariables.HZZ.deactivate(True)
        globalvariables.HWW.deactivate(True)
    if not config.countVHdecaytype:
        globalvariables.VH.deactivate(True)
    if not config.checklnu2qcharge:
        globalvariables.decayWWlplusnu2q.deactivate(True)
        globalvariables.decayWWlminusnu2q.deactivate(True)

    config.init()
    finishedinit = True
