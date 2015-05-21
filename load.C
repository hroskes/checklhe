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
        f->readevent()->print();
    }
}
