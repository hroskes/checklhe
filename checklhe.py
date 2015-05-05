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
        globalvariables.globalvariables.eventcounter = collections.Counter()
        if config.tree:
            globalvariables.globalvariables.rootfile = ROOT.TFile(file.replace(".lhe","",1) + '.root', 'recreate')
            globalvariables.globalvariables.tree = ROOT.TTree("tree", "tree")
        if config.makedecayanglestree:
            globalvariables.globalvariables.costheta1 = array.array('d', [0])
            globalvariables.globalvariables.costheta2 = array.array('d', [0])
            globalvariables.globalvariables.Phi       = array.array('d', [0])
            globalvariables.globalvariables.tree.Branch("costheta1", globalvariables.globalvariables.costheta1, "costheta1/D")
            globalvariables.globalvariables.tree.Branch("costheta2", globalvariables.globalvariables.costheta2, "costheta2/D")
            globalvariables.globalvariables.tree.Branch("Phi",       globalvariables.globalvariables.Phi,       "Phi/D")
        if config.makeZZmassestree:
            globalvariables.globalvariables.mZ1 = array.array('d', [0])
            globalvariables.globalvariables.mZ2 = array.array('d', [0])
            globalvariables.globalvariables.mH  = array.array('d', [0])
            globalvariables.globalvariables.tree.Branch("mZ1", globalvariables.globalvariables.mZ1, "mZ1/D")
            globalvariables.globalvariables.tree.Branch("mZ2", globalvariables.globalvariables.mZ2, "mZ2/D")
            globalvariables.globalvariables.tree.Branch("mH",  globalvariables.globalvariables.mH,  "mH/D")
        for line in f:
            linenumber += 1
            if "<event>" in line:
                if inevent:
                    raiseerror("Extra <event>! " + str(linenumber))
                    continue
                inevent = True
                ev = event.Event(linenumber)
                nleptons = 0
                continue
            if "</event>" in line:
                if not inevent:
                    raiseerror("Extra </event>! " + str(linenumber))
                    continue
                ev.finished()
                ev.process()
                check = ev.check()
                if check:
                    raiseerror(check)

                inevent = False
                continue
            if not inevent:
                continue

            if ev.firstline is None:
                ev.setfirstline(line)
                continue

            try:
                ev.addparticle(line)
            except IndexError:
                continue

        if config.tree:
            globalvariables.globalvariables.tree.Write()
            globalvariables.globalvariables.rootfile.Close()

    tab = "   "
    if inevent:
        print "No </event> at end!"
    print globalvariables.globalvariables.anyevent.printcount()
