import particletype

class ParticleCategory(set):
    def __init__(self, lst, Csymmetric = True):
        if not Csymmetric:
            print lst
        newlist = []
        for p in lst:
            type = particletype.ParticleType(p)
            newlist.append(type)
            if Csymmetric:
                newlist.append(-type)
        if not Csymmetric:
            print newlist
        super(ParticleCategory, self).__init__(newlist)

    def __contains__(self, particle):
        try:
            if super(ParticleCategory, self).__contains__(particle):
                return True
        except TypeError:
            pass
        try:
            return super(ParticleCategory, self).__contains__(particletype.ParticleType(particle))
        except ValueError:
            return False

    def __str__(self):
        return " ".join(str(p) for p in self)
