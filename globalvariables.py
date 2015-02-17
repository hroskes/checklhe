import particlecategory
import particle

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

startedinit = False
finishedinit = False

def init():
    global electrons, muons, taus, leptons, neutrinos, uptypequarks, downtypequarks, quarks, neutralbosons, W
    global decay4e, decay2e2mu, decay4mu, decay2e2tau, decay2mu2tau, decay4tau, decay4l, decay2l2nu, decay2l2q, decay4nu, decay2q2nu, decay4q
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

        decay4e = particle.DecayFamily([[11, 11, -11, -11]])
        decay4mu = particle.DecayFamily([[13, 13, -13, -13]])
        decay4tau = particle.DecayFamily([[15, 15, -15, -15]])
        decay2e2mu = particle.DecayFamily([[11, 13, -11, -13]])
        decay2e2tau = particle.DecayFamily([[11, 15, -11, -15]])
        decay2mu2tau = particle.DecayFamily([[13, 15, -13, -15]])
        decay4l = decay4e.union(decay4mu).union(decay4tau).union(decay2e2mu).union(decay2e2tau).union(decay2mu2tau)
        decay2l2q = particle.DecayFamily([[quarks, quarks, leptons, leptons]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0)
        decay2l2nu = particle.DecayFamily([[neutrinos, neutrinos, leptons, leptons]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0)
        decay2q2nu = particle.DecayFamily([[quarks, quarks, neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0)
        decay4q = particle.DecayFamily([[quarks, quarks, quarks, quarks]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0)
        decay4nu = particle.DecayFamily([[neutrinos, neutrinos, neutrinos, neutrinos]], charge = 0, leptonnumber = (0, 0, 0), baryonnumber = 0)

        finishedinit = True
