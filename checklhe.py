import sys

#https://root.cern.ch/phpBB3/viewtopic.php?t=3198
tempargv = sys.argv
sys.argv.insert(0, '-b')
import ROOT
del sys.argv[0]
#Try both ways
ROOT.gROOT.SetBatch(True)

import lhefile

for file in sys.argv[1:]:
    print file
    with lhefile.LHEFile(file) as f:
        for ev in f:
            ev.process()
            check = ev.check()
            if check:
                f.raiseerror(check)
