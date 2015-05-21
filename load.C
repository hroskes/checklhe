void load()
{
    gROOT->LoadMacro("particletype.C+");
    gROOT->LoadMacro("momentum.C+");
    gROOT->LoadMacro("particle.C+");
    gROOT->LoadMacro("event.C+");
    gROOT->LoadMacro("lhefile.C+");
    LHEFile *f = new LHEFile("VBFscalar33_decayed.lhe");
    f->readevent()->print();
}
