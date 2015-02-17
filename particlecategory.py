import particletype

class ParticleCategory(set):
    def __init__(self, lst):
        newlist = []        
        for p in lst:
            type = particletype.ParticleType(p)
            newlist.append(particletype.ParticleType(p))
            newlist.append(-type)
        super(ParticleCategory, self).__init__(newlist)

    def __contains__(self, particle):
        try:
            if super(ParticleCategory, self).__contains__(particle):
                return True
        except TypeError:
            try:
                return super(ParticleCategory, self).__contains__(particletype.ParticleType(particle))
            except ValueError:
                return False
