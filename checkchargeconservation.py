import particle
import config
import sys

for file in sys.argv[1:]:
    print file
    with open(file) as f:
        inevent = False
        linenumber = 0
        n4l  = 0
        nZZ4e = 0
        nZZ4mu = 0
        nZZ4tau = 0
        nZZ2e2mu = 0
        nZZ2e2tau = 0
        nZZ2mu2tau = 0
        nZZ2l2nu  = 0
        nZZ2q2nu = 0
        nZZ2l2q = 0
        nZZ4nu = 0
        nZZ4q = 0
        nevents = 0
        for line in f:
            linenumber += 1
            if "<event>" in line:
                if inevent:
                    print "Extra <event>!", linenumber
                inevent = True
                particle.newevent()
                counter = -1
                nleptons = 0
                nevents += 1
                continue
            if "</event>" in line:
                if not inevent:
                    print "Extra </event>!", linenumber
                for p in particle.particlelist:
                    if p is None:
                        continue

                if config.count4levents and len([p for p in particle.particlelist if p is not None and p.islepton()]) >= 4:
                    n4l += 1
                if config.countZZdecaytype and particle.higgs is not None:
                    Zs = particle.higgs.kids()
                    if all([Z.isZ() for Z in Zs]) and len(Zs) == 2:
                        n2e = 0
                        n2mu = 0
                        n2tau = 0
                        n2nu = 0
                        n2q = 0
                        for Z in Zs:
                            if all(p.ise() for p in Z.kids()):
                                n2e += 1
                            if all(p.ismu() for p in Z.kids()):
                                n2mu += 1
                            if all(p.istau() for p in Z.kids()):
                                n2tau += 1
                            if all(p.isneutrino() for p in Z.kids()):
                                n2nu += 1
                            if all(p.isquark() for p in Z.kids()):
                                n2q += 1
                        n2l = n2e + n2mu + n2tau
                        if n2e == 2:
                            nZZ4e += 1
                        if n2mu == 2:
                            nZZ4mu += 1
                        if n2tau == 2:
                            nZZ4tau += 1
                        if n2e == 1 and n2mu == 1:
                            nZZ2e2mu += 1
                        if n2e == 1 and n2tau == 1:
                            nZZ2e2tau += 1
                        if n2mu == 1 and n2tau == 1:
                            nZZ2mu2tau += 1
                        if n2l == 1 and n2q == 1:
                            nZZ2l2q += 1
                        if n2l == 1 and n2nu == 1:
                            nZZ2l2nu += 1
                        if n2q == 2:
                            nZZ4q += 1
                        if n2nu == 2:
                            nZZ4nu += 1
                        if n2q == 1 and n2nu == 1:
                            nZZ2q2nu += 1

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
