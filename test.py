import particle
import particletype
import globalvariables

if __name__ == "__main__":
    globalvariables.init()

    for a in globalvariables.decay4nu:
        for b in a.elements():
            print b,
        print 
