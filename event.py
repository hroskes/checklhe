import collections
import config

class OrderedCounter(collections.Counter, collections.OrderedDict):
    def __reversed__(self):
        result = self.__class__()
        for _ in reversed(self.keys()):
            result[_] = self[_]
        return result

    def elements(self):
        result = []
        for key in self:
            for i in range(self[key]):
                result.append(key)
        return result

class PrintableCounter(collections.Counter):
    def __str__(self):
        result = ''
        for item in self:
            if config.printreversed and item > item.reversed() and item.reversed() in self:
                continue
            result += "{}: {:>6}".format(item, self[item])
            if config.printreversed and item < item.reversed():
                result += "\t{}: {:>6}\tDelta = {:>4} = {:6.1f}%".format(item.reversed(), self[item.reversed()], self[item] - self[item.reversed()], 100.*(self[item] - self[item.reversed()])/self[item])
            result += "\n"
        return result
            

class Parton(int):
    def __str__(self):
        if self == 1:  return "d   "
        if self == 2:  return "u   "
        if self == 3:  return "s   "
        if self == 4:  return "c   "
        if self == 5:  return "b   "
        if self == -1: return "dbar"
        if self == -2: return "ubar"
        if self == -3: return "sbar"
        if self == -4: return "cbar"
        if self == -5: return "bbar"
        if self == 21: return "g   "
        raise ValueError("bad parton id! %i" % self)


class Event(object):
    def __init__(self):
        self.incoming = OrderedCounter()
        self.outgoing = OrderedCounter()
        self.frozen = False

    def addparticle(self, line):
        if self.frozen:
            raise RuntimeError("frozen, can't add particle!\n" + line)
        id = int(line.split()[0])
        status = int(line.split()[1])
        if abs(id) > 5 and id != 21:
            return
        if status == -1:
            self.incoming[Parton(id)] += 1
        elif status == 1:
            if config.outgoingmatters:
                self.outgoing[Parton(id)] += 1
        else:
            raise ValueError("Invalid status! " + line)

    def freeze(self):
        if sum(self.incoming.values()) == 2 and (sum(self.outgoing.values()) == 2 or not config.outgoingmatters):
            self.frozen = True
        else:
            raise IndexError("Not enough elements yet! %s %s" % (self.incoming, self.outgoing))

    def setweight(self, initline):
        if config.weighted:
            self.weight = float(initline.split()[2])
        else:
            self.weight = 1

    def __str__(self):
        if config.outgoingmatters:
            return "(" + " ".join(str(a) for a in self.incoming.elements()) + ") --> (" + " ".join(str(a) for a in self.outgoing.elements()) + ")"
        else:
            return "(" + " ".join(str(a) for a in self.incoming.elements()) + ") --> *"

    def __hash__(self):
        if config.ordermatters:
            immutabletype = tuple
        else:
            immutabletype = frozenset
        if not self.frozen:
            raise RuntimeError("not frozen, can't hash!\n" + line)
        return hash((immutabletype(self.incoming), immutabletype(self.outgoing)))

    def __eq__(self, other):
        return (self.incoming, self.outgoing, self.frozen) == (other.incoming, other.outgoing, other.frozen)

    def reversed(self):
        result = self.__class__()
        result.incoming = reversed(self.incoming)
        result.outgoing = self.outgoing
        result.freeze()
        return result

    def __cmp__(self, other):
        result = cmp(self.incoming.elements()[0], other.incoming.elements()[0])
        if not result:
            result = cmp(self.incoming.elements()[1], other.incoming.elements()[1])
        return result

    def beforereversed(self):
        return self < reversed(self)
