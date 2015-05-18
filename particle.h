#include "momentum.h"
class Particle : public ParticleType, public Momentum
{
    private:
        TString _line;
        Event *_ev;
        int _id;
        int _status;
        pair<int, int> _motherindices;
        pair<Particle*, Particle*> _mothers;
        vector<Particle*> _kids;
        int _color;
        int _anticolor;
        float _lhemass;
        float _lifetime;
        float _spin;
        Vertex _startvertex;
        Vertex _endvertex;
        vector<TString> _miscellaneouschecks;
    public:
        Particle(TString line, Event *ev);
        void setmothers();
        bool iskidof(Particle *potentialmother);
        void addkid(Particle *kid);
        Vertex *getendvertex();
        void setendvertex(Vertex *vertex);
};
