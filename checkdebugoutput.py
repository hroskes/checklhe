#A separate script to check the debug output of JHUGen
#uses config.counttauaseormu
import sys

#https://root.cern.ch/phpBB3/viewtopic.php?t=3198
tempargv = sys.argv
sys.argv.insert(0, '-b')
import ROOT
del sys.argv[0]
#Try both ways
ROOT.gROOT.SetBatch(True)

import config
import globalvariables
import particletype
import usefulstuff

config.checkhiggsdecaytype = False
config.countVHdecaytype = False
globalvariables.init()


def count2l2l(leptons):
    e = globalvariables.electrons
    mu = globalvariables.muons
    tau = globalvariables.taus
    flavors = [e, mu, tau]
    hasl = {f: {1: 0, -1: 0} for f in flavors}
    for p in leptons:
        for f in flavors:
            if p in f:
                hasl[f][p.charge()] += 1
    haslplm = {f: min(hasl[f][1], hasl[f][-1]) for f in flavors}
    npairs = sum(haslplm[f] for f in haslplm)
    if config.counttauaseormu:
        for f in hasl:
            for charge in hasl[f]:
                hasl[f][charge] -= haslplm[f]
        for f in [e, mu]:
            for charge in [1, -1]:
                while hasl[f][charge] and hasl[tau][-charge]:
                    hasl[f][charge] -= 1
                    hasl[tau][-charge] -= 1
                    npairs += 1
    return npairs >= 2


for file in sys.argv[1:]:
    print file
    with open(file) as f:
        inheader = True
        inevent = False
        linenumber = 0
        for line in f:
            linenumber += 1
            if inheader and "leptons in event" not in line:
                continue
            if "leptons in event" in line:
                inheader = False
                leptons = usefulstuff.printablelist()
                for lepton in line.split(":")[1].split():
                    leptons.append(particletype.ParticleType(lepton))
                shouldaccept = count2l2l(leptons)
                print leptons, "accept =", shouldaccept,
                continue
            if "found" in line:
                continue
            if "accept" in line:
                print "accept"
            if "reject" in line:
                print "reject"
            if "accept" in line and not shouldaccept or "reject" in line and shouldaccept:
                print "Wrong! " + str(linenumber)
