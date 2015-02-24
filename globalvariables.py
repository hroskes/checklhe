import particlecategory
import particle
import collections

momentumtolerance = 1e-4
masstolerance = 7e-2

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
particlemass = {1: 0,
                2: 0,
                3: 0,
                4: 0,
                5: 4.2,
                6: 173,
                11: 5.11e-4,
                12: 0,
                13: 0.10566,
                14: 0,
                15: 1.7768,
                16: 0,
                21: 0,
                22: 0,
                23: 91.1876,
                24: 80.385,
                25: None}     #Overwritten from the LHE header

eventcounter = collections.Counter()

startedinit = False
finishedinit = False

def init():
    global electrons, muons, taus, leptons, neutrinos, uptypequarks, downtypequarks, quarks, neutralbosons, W
    global decay4e, decay2e2mu, decay4mu, decay2e2tau, decay2mu2tau, decay4tau, decay4l, decay2l2nu, decay2l2q, decay4nu, decay2q2nu, decay4q, decaylnu2q
    global any4l, anyevent
    global decayfamilies4l, decayfamilies2l2nu, decayfamilies2l2q, decayfamilieslnu2q, decayfamiliestoplevel, decaysubcategories, decayfamilies
    global startedinit, finishedinit

    if not startedinit:
        startedinit = True

        electrons = particlecategory.ParticleCategory([11])
        muons = particlecategory.ParticleCategory([13])
        taus = particlecategory.ParticleCategory([15])
        leptons = electrons.union(muons).union(taus)
        neutrinos = particlecategory.ParticleCategory([12, 14, 16])
        uptypequarks = particlecategory.ParticleCategory([2, 4, 6])
        downtypequarks = particlecategory.ParticleCategory([1, 3, 5])
        quarks = uptypequarks.union(downtypequarks)
        neutralbosons = particlecategory.ParticleCategory([21, 22, 23, 25])
        W = particlecategory.ParticleCategory([24])

        decay4e = particle.DecayFamily([[11, 11, -11, -11]], name = "ZZ4e")
        decay4mu = particle.DecayFamily([[13, 13, -13, -13]], name = "ZZ4mu")
        decay4tau = particle.DecayFamily([[15, 15, -15, -15]], name = "ZZ4tau")
        decay2e2mu = particle.DecayFamily([[11, 13, -11, -13]], name = "ZZ2e2mu")
        decay2e2tau = particle.DecayFamily([[11, 15, -11, -15]], name = "ZZ2e2tau")
        decay2mu2tau = particle.DecayFamily([[13, 15, -13, -15]], name = "ZZ2mu2tau")
        decayfamilies4l = [decay4e, decay4mu, decay4tau, decay2e2mu, decay2e2tau, decay2mu2tau]

        decay2e2q = particle.DecayFamily([[electrons, electrons, quarks, quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "ZZ2e2q")
        decay2mu2q = particle.DecayFamily([[muons, muons, quarks, quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "ZZ2mu2q")
        decay2tau2q = particle.DecayFamily([[taus, taus, quarks, quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "ZZ2tau2q")
        decayfamilies2l2q = [decay2e2q, decay2mu2q, decay2tau2q]

        decay2e2nu = particle.DecayFamily([[electrons, electrons, neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "ZZ(WW)2e2nu")
        decay2mu2nu = particle.DecayFamily([[muons, muons, neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "ZZ(WW)2mu2nu")
        decay2tau2nu = particle.DecayFamily([[taus, taus, neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "ZZ(WW)2tau2nu")
        decayemu2nu = particle.DecayFamily([[electrons, muons, neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "WWemu2nu")
        decayetau2nu = particle.DecayFamily([[electrons, taus, neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "WWetau2nu")
        decaymutau2nu = particle.DecayFamily([[muons, taus, neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "WWmutau2nu")
        decayfamilies2l2nu = [decay2e2nu, decay2mu2nu, decay2tau2nu, decayemu2nu, decayetau2nu, decaymutau2nu]

        decayenuqq = particle.DecayFamily([[electrons, neutrinos, quarks, quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "ZZenuqq")
        decaymunuqq = particle.DecayFamily([[muons, neutrinos, quarks, quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "ZZmunuqq")
        decaytaunuqq = particle.DecayFamily([[taus, neutrinos, quarks, quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "ZZtaunuqq")
        decayfamilieslnuqq = [decayenuqq, decaymunuqq, decaytaunuqq]


        decay4l = particle.DecayFamily([[leptons, leptons, leptons, leptons]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "ZZ4l",
                                       subcategories = decayfamilies4l)
        decay2l2q = particle.DecayFamily([[quarks, quarks, leptons, leptons]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "ZZ2l2q",
                                         subcategories = decayfamilies2l2q)
        decay2l2nu = particle.DecayFamily([[neutrinos, neutrinos, leptons, leptons]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "ZZ(WW)2l2nu",
                                          subcategories = decayfamilies2l2nu)
        decaylnu2q = particle.DecayFamily([[leptons, neutrinos, quarks, quarks]], charge = 0, leptonnumber = (0,0,0), baryonnumber = 0, name = "WWlnu2q",
                                          subcategories = decayfamilieslnuqq)

        decay2q2nu = particle.DecayFamily([[quarks, quarks, neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "ZZ2q2nu")
        decay4q = particle.DecayFamily([[quarks, quarks, quarks, quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "ZZ(WW)4q")
        decay4nu = particle.DecayFamily([[neutrinos, neutrinos, neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "ZZ4nu")

        decayfamiliestoplevel = [decay4l, decay2l2q, decay2l2nu, decay4q, decay4nu, decay2q2nu, decaylnu2q]
        decaysubcategories = decayfamilies4l + decayfamilies2l2q + decayfamilies2l2nu + decayfamilieslnuqq
        decayfamilies = decayfamiliestoplevel + decaysubcategories

        any4l = particle.EventCount("4l", [decay4l])
        anyevent = particle.EventCount("total", [any4l, decay2l2q, decay2l2nu, decay2q2nu, decay4q, decay4nu, decaylnu2q])

        finishedinit = True
