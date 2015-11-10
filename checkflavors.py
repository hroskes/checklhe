import sys
import event

def checkflavors(file):
    counter = event.MyCounter()
    with open(file) as f:
        inevent, sawinitline = False, False
        for line in f:
            if not inevent and "<event>" in line:
                ev = event.Event()
                inevent, sawinitline = True, False
                continue
            elif "</event>" in line:
                ev.freeze()
                counter[ev] += 1
                inevent = False
                continue
            elif not inevent:
                continue
            elif not sawinitline:
                sawinitline = True
                continue

            ev.addparticle(line)

    print counter

if __name__ == '__main__':
    checkflavors(sys.argv[1])
