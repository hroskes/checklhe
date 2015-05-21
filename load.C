void load()
{
    if (
      gROOT->LoadMacro("particletype.C+") == 0 &&
      gROOT->LoadMacro("momentum.C+") == 0 &&
      gROOT->LoadMacro("particle.C+") == 0 &&
      gROOT->LoadMacro("event.C+") == 0 &&
      gROOT->LoadMacro("lhefile.C+") == 0
    )
    {
        LHEFile *f = new LHEFile("VBFscalar33_decayed.lhe");
        Event *ev;
        while (ev = f->readevent())
        {
            ev->boosttocom(ev->higgs());
            ev->rotatetozx(ev->getparticle(6), ev->getparticle(8));
            ev->print();
            //return;
        }
    }
}
