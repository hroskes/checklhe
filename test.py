import particle
import particletype
import globalvariables

if __name__ == "__main__":
    globalvariables.init()

    for a in sorted(globalvariables.decay2l2q):
        for b in sorted(a.elements()):
            print b,
        print 
    print particle.ParticleCounter([1, -1, 6, -6]) in globalvariables.decay4q
    print particle.ParticleCounter([1, -3, 6, -6]) in globalvariables.decay4q
    print particle.ParticleCounter([1, -2, 6, -6]) in globalvariables.decay4q
