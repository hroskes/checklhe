import particle
import event
import globalvariables
import config
import sys
import collections
import re

globalvariables.init()

for file in sys.argv[1:]:
    print file
    with open(file) as f:
        inevent = False
        linenumber = 0
        globalvariables.nevents = 0
        globalvariables.n4l = 0
        globalvariables.decaycounter = collections.Counter()
        globalvariables.foundhiggsmass = False
        for line in f:
            linenumber += 1
            if not inevent and globalvariables.particlemass[25] is None:
                match = re.search(r"Resonance.*mass *=([ 1234567890.]*)", line)
                if match:
                    globalvariables.particlemass[25] = float(match.group(1))
                    print "Read higgs mass from file: %s GeV" % globalvariables.particlemass[25]
            if "<event>" in line:
                if inevent:
                    print "Extra <event>!", linenumber
                inevent = True
                particle.newevent()
                counter = -1
                nleptons = 0
                continue
            if "</event>" in line:
                if not inevent:
                    print "Extra </event>!", linenumber
                ev = event.Event(particle.particlelist, linenumber)
                if ev.check():
                    raise IOError(ev.check())

                inevent = False
                continue
            if not inevent:
                continue

            counter += 1
            try:
                p = particle.Particle(line)
            except ValueError:
                continue

    tab = "   "
    if inevent:
        print "No </event> at end!"
    print globalvariables.nevents, "events"
    print tab, globalvariables.n4l, "4l events (%s%%)" % (100.0 * globalvariables.n4l / globalvariables.nevents)
    for family in globalvariables.decayfamilies:
        print family.printcount()
