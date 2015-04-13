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
    if config.counttauaseormu:
        for f in hasl:
            for charge in hasl[f]:
                hasl[f][charge] -= haslplm[f]
        for f in [e, mu]:
            for charge in [1, -1]:
                while hasl[f][charge] and hasl[tau][-charge]:
                    hasl[f][charge] -= 1
                    hasl[tau][-charge] -= 1
                    haslplm[f] += 1
                while hasl[f][charge] and haslplm[tau]:
                    hasl[f][charge] -= 1
                    #disassemble the tau pair, e.g. for f-, take apart tau+tau- and put it into tau+f-
                    #and then put tau- back in hasl
                    haslplm[tau] -= 1
                    hasl[tau][charge] += 1
                    haslplm[f] += 1
    return sum(haslplm[f] for f in haslplm) >= 2

if __name__ == "__main__":
    #no need for these here, they make init take longer
    config.checkhiggsdecaytype = False
    config.countVHdecaytype = False

    globalvariables.init()

    shouldaccept = {True: "accept", False: "reject"}

    for file in sys.argv[1:]:
        print file
        with open(file) as f:
            inheader = True
            linenumber = 0
            acceptcounter = 0
            for line in f:
                linenumber += 1
                if inheader and "leptons in event" not in line:
                    continue
                if "leptons in event" in line:
                    inheader = False
                    leptons = usefulstuff.printablelist()
                    for lepton in line.split(":")[1].split():
                        leptons.append(particletype.ParticleType(lepton))
                    hasOSSF = count2l2l(leptons)
                    print leptons, shouldaccept[hasOSSF],
                    continue
                if "found" in line:
                    continue
                if "accept" in line:
                    print "accept"
                    acceptcounter += 1
                if "reject" in line and "The number of rejected events exceeds" not in line:
                    print "reject"
                if "accept" in line and not hasOSSF or "reject" in line and "The number of rejected events exceeds" not in line and hasOSSF:
                    print "Wrong! " + str(linenumber)
                if "Acceptance Counter:" in line:
                    naccepted = int(line.split(":")[1])
                    if acceptcounter != naccepted:
                        print "Inconsistent!", acceptcounter, "events accepted but Acceptance Counter =", naccepted
