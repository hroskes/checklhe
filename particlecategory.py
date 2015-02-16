import particletype

class ParticleCategory(frozenset):
    def __init__(self, lst):
        newlst = []
        for p in lst:
            type = particletype.ParticleType(p)
            newlst.append(particletype.ParticleType(p))
            newlst.append(-type)
        print len(newlst)
        print len(frozenset(newlst))
        super(ParticleCategory, self).__init__(newlst)
        print len(self)

    def __contains__(self, particle):
        try:
            if super(ParticleCategory, self).__contains__(particle):
                return True
        except TypeError:
            try:
                return super(ParticleCategory, self).__contains__(particletype.ParticleType(particle))
            except ValueError:
                return False
