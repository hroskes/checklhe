import particlecategory
import particle
import config
import collections

eventcounter = collections.Counter()

startedinit = False
finishedinit = False

def init():
    global electrons, muons, taus, leptons, neutrinos, uptypequarks, downtypequarks, quarks, neutralbosons, weakbosons, gluon, photon, Z, W, higgs
    global decayZZ4l, decayZZ2l2nu, decayZZ2l2q, decayZZ4nu, decayZZ2q2nu, decayZZ4q
    global decayWW2l2nu, decayWW4q, decayWWlnu2q
    global HZZ, HWW, ZH, WH, VH
    global any2l2l, any4l, anyevent, leptoncount
    global decayfamiliesZZ4l, decayfamiliesZZ2l2nu, decayfamiliesWW2l2nu, decayfamiliesZZ2l2q, decayfamiliesWWlnu2q
    global decayfamiliestoplevel
    global startedinit, finishedinit

    if not startedinit:
        startedinit = True

        #Particle categories
        neutralbosons = particlecategory.ParticleCategory([21, 22, 23, 25, 32, 39], Csymmetric = False)
        electrons = particlecategory.ParticleCategory([11])
        muons = particlecategory.ParticleCategory([13])
        taus = particlecategory.ParticleCategory([15])
        leptons = electrons.union(muons).union(taus)
        neutrinos = particlecategory.ParticleCategory([12, 14, 16])
        uptypequarks = particlecategory.ParticleCategory([2, 4, 6])
        downtypequarks = particlecategory.ParticleCategory([1, 3, 5])
        quarks = uptypequarks.union(downtypequarks)
        gluon = particlecategory.ParticleCategory([21])
        photon = particlecategory.ParticleCategory([22])
        weakbosons = particlecategory.ParticleCategory([23, 24])
        Z = particlecategory.ParticleCategory([23])
        W = particlecategory.ParticleCategory([24])
        higgs = particlecategory.ParticleCategory([25, 32, 39])
        print "initialized particle categories"

        if config.counthiggsdecaytype:

            #4l decays by flavor
            decayZZ4e = particle.DecayFamily([[11, 11, -11, -11]], name = "H --> ZZ --> 4e")
            decayZZ4mu = particle.DecayFamily([[13, 13, -13, -13]], name = "H --> ZZ --> 4mu")
            decayZZ4tau = particle.DecayFamily([[15, 15, -15, -15]], name = "H --> ZZ --> 4tau")
            decayZZ2e2mu = particle.DecayFamily([[11, 13, -11, -13]], name = "H --> ZZ --> 2e2mu")
            decayZZ2e2tau = particle.DecayFamily([[11, 15, -11, -15]], name = "H --> ZZ --> 2e2tau")
            decayZZ2mu2tau = particle.DecayFamily([[13, 15, -13, -15]], name = "H --> ZZ --> 2mu2tau")
            decayfamiliesZZ4l = [decayZZ4e, decayZZ4mu, decayZZ4tau, decayZZ2e2mu, decayZZ2e2tau, decayZZ2mu2tau]

            #2l2q decays by flavor
            decayZZ2e2q = particle.DecayFamily([[electrons, electrons, quarks, quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 2e2q")
            decayZZ2mu2q = particle.DecayFamily([[muons, muons, quarks, quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 2mu2q")
            decayZZ2tau2q = particle.DecayFamily([[taus, taus, quarks, quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 2tau2q")
            decayfamiliesZZ2l2q = [decayZZ2e2q, decayZZ2mu2q, decayZZ2tau2q]

            #2l2nu decays by flavor
            decayZZ2e2nu = particle.DecayFamily([[electrons, electrons, neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 2e2nu")
            decayZZ2mu2nu = particle.DecayFamily([[muons, muons, neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 2mu2nu")
            decayZZ2tau2nu = particle.DecayFamily([[taus, taus, neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 2tau2nu")
            decayfamiliesZZ2l2nu = [decayZZ2e2nu, decayZZ2mu2nu, decayZZ2tau2nu]
            decayWW2e2nu = particle.DecayFamily([[electrons, electrons, neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW --> 2e2nu")
            decayWW2mu2nu = particle.DecayFamily([[muons, muons, neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW --> 2mu2nu")
            decayWW2tau2nu = particle.DecayFamily([[taus, taus, neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW --> 2tau2nu")
            decayWWemu2nu = particle.DecayFamily([[electrons, muons, neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW -->emu2nu")
            decayWWetau2nu = particle.DecayFamily([[electrons, taus, neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW -->etau2nu")
            decayWWmutau2nu = particle.DecayFamily([[muons, taus, neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW -->mutau2nu")
            decayfamiliesWW2l2nu = [decayWW2e2nu, decayWW2mu2nu, decayWW2tau2nu, decayWWemu2nu, decayWWetau2nu, decayWWmutau2nu]

            #lnu2q decays by flavor
            if config.checklnu2qcharge:
                decayWWlplusnu2q = particle.DecayFamily([[[-11], neutrinos, quarks, quarks], [[-13], neutrinos, quarks, quarks], [[-15], neutrinos, quarks, quarks]],
                                                                                         charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW --> l+nu2q", Csymmetric = False)
                decayWWlminusnu2q = particle.DecayFamily([[[+11], neutrinos, quarks, quarks], [[+13], neutrinos, quarks, quarks], [[+15], neutrinos, quarks, quarks]],
                                                                                         charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW --> l-nu2q", Csymmetric = False)
                decayfamiliesWWlnu2q = [decayWWlplusnu2q, decayWWlminusnu2q]
            else:
                decayWWenu2q = particle.DecayFamily([[electrons, neutrinos, quarks, quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW --> enu2q")
                decayWWmunu2q = particle.DecayFamily([[muons, neutrinos, quarks, quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW --> munu2q")
                decayWWtaunu2q = particle.DecayFamily([[taus, neutrinos, quarks, quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW --> taunu2q")
                decayfamiliesWWlnu2q = [decayWWenu2q, decayWWmunu2q, decayWWtaunu2q]

            #top level decay categories
            decayZZ4l = particle.DecayFamily([[leptons, leptons, leptons, leptons]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 4l",
                                           subcategories = decayfamiliesZZ4l)
            decayZZ2l2q = particle.DecayFamily([[quarks, quarks, leptons, leptons]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 2l2q",
                                             subcategories = decayfamiliesZZ2l2q)
            decayZZ2l2nu = particle.DecayFamily([[neutrinos, neutrinos, leptons, leptons]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 2l2nu",
                                              subcategories = decayfamiliesZZ2l2nu)
            decayWW2l2nu = particle.DecayFamily([[neutrinos, neutrinos, leptons, leptons]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW --> 2l2nu",
                                              subcategories = decayfamiliesWW2l2nu)
            decayWWlnu2q = particle.DecayFamily([[leptons, neutrinos, quarks, quarks]], charge = 0, leptonnumber = (0,0,0), baryonnumber = 0, name = "H --> WW -->lnu2q",
                                              subcategories = decayfamiliesWWlnu2q)
            decayZZ2q2nu = particle.DecayFamily([[quarks, quarks, neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 2q2nu")
            decayZZ4q = particle.DecayFamily([[quarks, quarks, quarks, quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 4q")
            decayWW4q = particle.DecayFamily([[quarks, quarks, quarks, quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> WW --> 4q")
            decayZZ4nu = particle.DecayFamily([[neutrinos, neutrinos, neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "H --> ZZ --> 4nu")

            #Higgs decay families
            HZZ = particle.DecayFamily([[Z, Z]], name = "H --> ZZ", subcategories = [decayZZ4l, decayZZ2l2q, decayZZ2l2nu, decayZZ4q, decayZZ4nu])
            HWW = particle.DecayFamily([[W, W]], charge = 0, name = "H --> WW", subcategories = [decayWW2l2nu, decayWW4q, decayWWlnu2q])
            decayfamiliestoplevel = [HZZ, HWW]

            print "initialized Higgs decay"

        if config.countVHdecaytype:

            ################
            #      VH      #
            ################

            #Z 2l decay families
            Zdecay2e = particle.DecayFamily([[electrons, electrons]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "Z --> 2e")
            Zdecay2mu = particle.DecayFamily([[muons, muons]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "Z --> 2mu")
            Zdecay2tau = particle.DecayFamily([[taus, taus]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "Z --> 2tau")
            Zdecayfamilies2l = [Zdecay2e, Zdecay2mu, Zdecay2tau]

            #Wminus lnu decay families
            Wminusdecayenu = particle.DecayFamily([[electrons, neutrinos]], charge = -1, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "W- --> enu")
            Wminusdecaymunu = particle.DecayFamily([[muons, neutrinos]], charge = -1, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "W- --> munu")
            Wminusdecaytaunu = particle.DecayFamily([[taus, neutrinos]], charge = -1, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "W- --> taunu")
            Wminusdecayfamilieslnu = [Wminusdecayenu, Wminusdecaymunu, Wminusdecaytaunu]

            #Wplus lnu decay families
            Wplusdecayenu = particle.DecayFamily([[electrons, neutrinos]], charge = 1, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "W+ --> enu")
            Wplusdecaymunu = particle.DecayFamily([[muons, neutrinos]], charge = 1, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "W+ --> munu")
            Wplusdecaytaunu = particle.DecayFamily([[taus, neutrinos]], charge = 1, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "W+ --> taunu")
            Wplusdecayfamilieslnu = [Wplusdecayenu, Wplusdecaymunu, Wplusdecaytaunu]

            #VH decay families
            Zdecay2l = particle.DecayFamily([[leptons, leptons]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "Z --> 2l",
                                            subcategories = Zdecayfamilies2l)
            Zdecay2q = particle.DecayFamily([[quarks, quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "Z --> 2q")
            Zdecay2nu = particle.DecayFamily([[neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "Z --> 2nu")
            Wminusdecaylnu = particle.DecayFamily([[leptons, neutrinos]], charge = -1, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "W- --> lnu",
                                                  subcategories = Wminusdecayfamilieslnu)
            Wplusdecaylnu = particle.DecayFamily([[leptons, neutrinos]], charge = +1, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "W+ --> lnu",
                                                 subcategories = Wplusdecayfamilieslnu)
            Wminusdecay2q = particle.DecayFamily([[quarks, quarks]], charge = -1, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "W- --> 2q")
            Wplusdecay2q = particle.DecayFamily([[quarks, quarks]], charge = 1, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "W+ --> 2q")

            Zdecaycategories = [Zdecay2l, Zdecay2q, Zdecay2nu]
            ZH = particle.DecayFamily([], name = "ZH", subcategories = Zdecaycategories)
            Wdecaycategories = [Wminusdecaylnu, Wplusdecaylnu, Wminusdecay2q, Wplusdecay2q]
            WH = particle.DecayFamily([], name = "WH", subcategories = Wdecaycategories)

            VH = particle.EventCount("VH", [ZH, WH])

            print "initialized VH decay"

        #big categories
        leptoncount = {}
        for i in range(10):
            leptoncount[i] = particle.EventCount("exactly" + str(i) + "l", [])

        any2l2lsubcats = []
        if config.counthiggsdecaytype:
            any2l2lsubcats.append(decayZZ4l)
        any2l2l = particle.EventCount("2l2l", any2l2lsubcats)
        any4l = particle.EventCount("4l", [any2l2l, leptoncount[4]])

        anyeventsubcats = [(leptoncount[i] if i != 4 else any4l) for i in leptoncount]
        if config.counthiggsdecaytype:
            anyeventsubcats += [HZZ, HWW]
        if config.countVHdecaytype:
            anyeventsubcats += [VH]
        anyevent = particle.EventCount("total", anyeventsubcats)

        config.init()
        finishedinit = True
