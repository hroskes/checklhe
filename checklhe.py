import sys

#https://root.cern.ch/phpBB3/viewtopic.php?t=3198
tempargv = sys.argv
sys.argv.insert(0, '-b')
import ROOT
del sys.argv[0]
#Try both ways
ROOT.gROOT.SetBatch(True)

import particle
import event
import globalvariables
import config
import collections
import array
import re

globalvariables.init()

def raiseerror(msg):
    if config.raiseerror:
        raise IOError(msg)
    else:
        print msg

for file in sys.argv[1:]:
    print file
    with open(file) as f:
        inevent = False
        firstline = None
        linenumber = 0
        globalvariables.eventcounter = collections.Counter()
        if config.tree:
            globalvariables.rootfile = ROOT.TFile(file.replace(".lhe","",1) + '.root', 'recreate')
            globalvariables.tree = ROOT.TTree("tree", "tree")
        if config.makedecayanglestree:
            globalvariables.costheta1 = array.array('d', [0])
            globalvariables.costheta2 = array.array('d', [0])
            globalvariables.Phi       = array.array('d', [0])
            globalvariables.tree.Branch("costheta1", globalvariables.costheta1, "costheta1/D")
            globalvariables.tree.Branch("costheta2", globalvariables.costheta2, "costheta2/D")
            globalvariables.tree.Branch("Phi",       globalvariables.Phi,       "Phi/D")
        if config.makeZZmassestree:
            globalvariables.mZ1 = array.array('d', [0])
            globalvariables.mZ2 = array.array('d', [0])
            globalvariables.mH  = array.array('d', [0])
            globalvariables.tree.Branch("mZ1", globalvariables.mZ1, "mZ1/D")
            globalvariables.tree.Branch("mZ2", globalvariables.mZ2, "mZ2/D")
            globalvariables.tree.Branch("mH",  globalvariables.mH,  "mH/D")
        for line in f:
            linenumber += 1
            if "<event>" in line:
                if inevent:
                    raiseerror("Extra <event>! " + str(linenumber))
                inevent = True
                eventline = linenumber
                particle.newevent()
                counter = -1
                nleptons = 0
                continue
            if "</event>" in line:
                if not inevent:
                    raiseerror("Extra </event>! " + str(linenumber))
                    continue
                ev = event.Event(eventline, firstline, particle.particlelist)
                firstline = None
                ev.process()
                check = ev.check()
                if check:
                    raiseerror(check)

                inevent = False
                continue
            if not inevent:
                continue

            if firstline is None:
                firstline = line
                continue

            counter += 1
            try:
                p = particle.Particle(line)
            except IndexError:
                continue

        if config.tree:
            globalvariables.tree.Write()
            globalvariables.rootfile.Close()

    tab = "   "
    if inevent:
        print "No </event> at end!"
    print globalvariables.anyevent.printcount()
