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

    nZZ4l = nZZ4e + nZZ4mu + nZZ4tau + nZZ2e2mu + nZZ2e2tau + nZZ2mu2tau
    tab = "   "
    if inevent:
        print "No </event> at end!"
    print nevents, "events"
    print tab, n4l, "4l events (%s%%)" % (100.0 * n4l / nevents)
    print tab, tab, nZZ4l, "ZZ4l events (%s%%)" % (100.0 * nZZ4l / nevents)
    print tab, tab, tab, nZZ4e, "4e events (%s%%)" % (100.0 * nZZ4e / nevents)
    print tab, tab, tab, nZZ4mu, "4mu events (%s%%)" % (100.0 * nZZ4mu / nevents)
    print tab, tab, tab, nZZ4tau, "4tau events (%s%%)" % (100.0 * nZZ4tau / nevents)
    print tab, tab, tab, nZZ2e2mu, "2e2mu events (%s%%)" % (100.0 * nZZ2e2mu / nevents)
    print tab, tab, tab, nZZ2e2tau, "2e2tau events (%s%%)" % (100.0 * nZZ2e2tau / nevents)
    print tab, tab, tab, nZZ2mu2tau, "2mu2tau events (%s%%)" % (100.0 * nZZ2mu2tau / nevents)
    print tab, nZZ2l2nu, "ZZ2l2nu events (%s%%)" % (100.0 * nZZ2l2nu / nevents)
    print tab, nZZ2l2q, "ZZ2l2q events (%s%%)" % (100.0 * nZZ2l2q / nevents)
    print tab, nZZ4q, "ZZ4q events (%s%%)" % (100.0 * nZZ4q / nevents)
    print tab, nZZ4nu, "ZZ4nu events (%s%%)" % (100.0 * nZZ4nu / nevents)
    print tab, nZZ2q2nu, "ZZ2q2nu events (%s%%)" % (100.0 * nZZ2q2nu / nevents)
