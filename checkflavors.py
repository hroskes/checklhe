import sys
import event

maxevents = 99999999999999999999

def checkflavors(file):
    counter = event.PrintableCounter()
    with open(file) as f:
        nevents = 0
        inevent, sawinitline = False, False
        for line in f:
            if not inevent and "<event>" in line:
                ev = event.Event()
                inevent, sawinitline = True, False
                continue
            elif "</event>" in line:
                ev.freeze()
                counter[ev] += ev.weight
                nevents += 1
                inevent = False
                if nevents >= maxevents:
                    break
                continue
            elif not inevent:
                continue
            elif not sawinitline:
                sawinitline = True
                ev.setweight(line)
                continue

            ev.addparticle(line)

    print counter

if __name__ == '__main__':
    checkflavors(sys.argv[1])
