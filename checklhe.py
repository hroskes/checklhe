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
        globalvariables.eventcounter = collections.Counter()
        globalvariables.foundhiggsmass = False
        for line in f:
            linenumber += 1
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
    print globalvariables.anyevent.printcount()
