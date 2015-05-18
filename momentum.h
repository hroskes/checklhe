#include "TLorentzVector.h"

class Momentum : public TLorentzVector
{
    private:
        Event _ev;
    public:
        Momentum(int ev, double px, double py, double pz, double E);
        ClassDef(Momentum, 1); //name
};

