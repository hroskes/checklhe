import particlecategory
import particle
import collections

momentumtolerance = 1e-4
masstolerance = 5e-2

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

decaycounter = collections.Counter()
nevents = 0
n4l = 0

electrons = None
muons = None
taus = None
leptons = None
neutrinos = None
uptypequarks = None
downtypequarks = None
quarks = None
neutralbosons = None
W = None

decay4e = None
decay2e2mu = None
decay4mu = None
decay2e2tau = None
decay2mu2tau = None
decay4tau = None
decay4l = None
decay2l2nu = None
decay2l2q = None
decay4nu = None
decay2q2nu = None
decay4q = None

decayfamilies4l = None
decayfamilies = None

startedinit = False
finishedinit = False

def init():
    global electrons, muons, taus, leptons, neutrinos, uptypequarks, downtypequarks, quarks, neutralbosons, W
    global decay4e, decay2e2mu, decay4mu, decay2e2tau, decay2mu2tau, decay4tau, decay4l, decay2l2nu, decay2l2q, decay4nu, decay2q2nu, decay4q
    global decayfamilies4l, decayfamilies
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

        decay4l = particle.DecayFamily([[leptons, leptons, leptons, leptons]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "ZZ4l",
                                       subcategories = decayfamilies4l)
        decay2l2q = particle.DecayFamily([[quarks, quarks, leptons, leptons]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "ZZ2l2q")
        decay2l2nu = particle.DecayFamily([[neutrinos, neutrinos, leptons, leptons]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "ZZ2l2nu")
        decay2q2nu = particle.DecayFamily([[quarks, quarks, neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "ZZ2q2nu")
        decay4q = particle.DecayFamily([[quarks, quarks, quarks, quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "ZZ4q")
        decay4nu = particle.DecayFamily([[neutrinos, neutrinos, neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0, name = "ZZ4nu")

        decayfamilies = [decay4l, decay2l2q, decay2l2nu, decay4q, decay4nu, decay2q2nu]

        finishedinit = True
