import collections
import ROOT
import config
import globalvariables
import event
import particle

class LHEFile:
    def __init__(self, filename):
        globalvariables.init()
        if filename[-4:] != ".lhe":
            raise ValueError(filename + " does not end in .lhe")
        self.filename = filename
        self.f = open(filename)
        self.nevents = 0
        self.linenumber = 0

    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        print "   ", self.nevents, "events"
        self.f.close()

    def raiseerror(self, msg):
        if config.raiseerror:
            raise IOError(msg)
        else:
            print msg

    def readevent(self):
        while "<event>" not in self.nextline():
            if not self.line:     #eof
                return None
            if "</event>" in self.line:
                self.raiseerror("Extra </event>! " + str(linenumber))
        ev = event.Event(self.linenumber)
        ev.setfirstline(self.nextline())
        while "</event>" not in self.nextline():
            if not self.line:
                self.raiseerror("File ends in the middle of an event!")
                return None
            if "<event>" in self.line:
                self.raiseerror("Extra </event>! " + str(linenumber))
            try:
                ev.addparticle(self.line)
            except particle.BadParticleLineError:
                continue
        ev.finished()
        self.nevents += 1
        return ev

    def nextline(self):
        self.linenumber += 1
        self.line = self.f.readline()
        return self.line

    def __iter__(self):
        return self
    def next(self):
        ev = self.readevent()
        if ev is not None:
            return ev
        raise StopIteration
