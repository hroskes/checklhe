class BadParticleLineException: public runtime_error {
    public:
        BadParticleLineException(TString particleline)
            : line(particleline), runtime_error(particleline)
        {}

    virtual const char* what() const throw()
    {
        return line + "\nis an invalid particle line!";
    }

    private:
        TString line;
};

Particle::Particle(TString line, Event *ev) :
    Momentum(_ev, 0, 0, 0, 0), ParticleType()
{
    _line = line;
    _ev = ev;
    vector<int> intdata;
    vector<float> floatdata;
    for (int i = 0; i < 6; i++)
    {
        TString part = nPart(i, line);
        if (! part.IsDigit())
            throw BadParticleLineException(line);
        intdata.push_back(part.Atoi());
    }
    for (int i = 6; i < 13; i++)
    {
        TString part = nPart(i, line);
        if (! part.IsFloat())
            throw BadParticleLineException(line);
        floatdata.push_back(part.Atof());
    }

    _id = intdata[0];
    init(_id);
    _status = intdata[1];
    _motherindices = make_pair(intdata[2], intdata[3]);
    _mothers = make_pair((Particle*)0, (Particle*)0);
    _kids = vector<Particle*>;
    _color = intdata[4];
    _anticolor = intdata[5];
    SetPxPyPzE(floatdata[0], floatdata[1], floatdata[2], floatdata[3]);
    _lhemass = floatdata[4];
    _lifetime = floatdata[5];
    _spin = floatdata[6];

    _ev->particlelist.push_back(this);
}

void setmothers()
{
    if ((mothers.first || ! motherindices.first) && (mothers.last || ! motherindices.last))
        continue;
    _mothers = make_pair(_ev->particlelist[_motherindices.first], _ev->particlelist[_motherindices.last]);
    _mothers.first->setmothers();
    _mothers.last->setmothers();
    _mothers.first->addkid(this);
    _mothers.last->addkid(this);

    _startvertex = _ev->getvertex(_mothers);
    _endvertex = 0;
    if (_mothers.first != 0)
    {
        if (_mothers.first->getendvertex() == 0)
            _mothers.first->setendvertex(_startvertex);
        else if (_mothers.first->getendvertex() != _startvertex)
            _miscellaneouschecks.push_back(_mothers.first->str() + "decays in multiple vertices!");
    }
    if (_mothers.last != 0 && _mothers.last != _mothers.first)
    {
        if (_mothers.last->getendvertex() == 0)
            _mothers.last->setendvertex(_startvertex);
        else if (_mothers.last->getendvertex() != _startvertex)
            _miscellaneouschecks.push_back(_mothers.last->str() + "decays in multiple vertices!");
    }
    if (_startvertex != 0)
        _startvertex->addkid(this);

    if (_color != 0)
        _ev->getcolor(_color)->addparticle(this);
    if (_anticolor != 0)
        _ev->getcolor(_anticolor)->addparticle(this);
}

bool iskidof(Particle *potentialmother)
{
    return (self._mothers.first == potentialmother || self._mothers.second == potentialmother);
}
void addkid(Particle *kid)
{
    for(std::vector<Particle*>::iterator it = _kids.begin(); it != _kids.end(); ++it)
        if ((*it) == kid)
            return;
    _kids->push_back(kid);
}

Vertex *getendvertex()
{
    return _endvertex;
}
void setendvertex(Vertex *vertex)
{
    _endvertex = vertex;
}

float lhemass()
{
    return _lhemass;
}
