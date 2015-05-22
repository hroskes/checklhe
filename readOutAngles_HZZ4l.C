void readOutAngles_HZZ4l(TString filename)
{
    gROOT->LoadMacro("particletype.C+");
    gROOT->LoadMacro("momentum.C+");
    gROOT->LoadMacro("particle.C+");
    gROOT->LoadMacro("event.C+");
    gROOT->LoadMacro("lhefile.C+");

    LHEFile *fin = new LHEFile(filename);
    TFile *fout = TFile::Open(filename.ReplaceAll(".lhe",".root"));
    TTree *t = new TTree("SelectedTree", "SelectedTree");

    double costheta1, costheta2, Phi, costhetastar, Phi1;
    t->Branch("costheta1",&costheta1,"costheta1/D");
    t->Branch("costheta2",&costheta2,"costheta2/D");
    t->Branch("Phi",&Phi,"Phi/D");
    t->Branch("costhetastar",&costhetastar,"costhetastar/D");
    t->Branch("Phi1",&Phi1,"Phi1/D");

    Event *ev;
    while (ev = fin->readevent())
    {
        ev->getZZ4langles(costheta1, costheta2, Phi, costhetastar, Phi1);
        t->Fill();
    }
    delete fin;
    t->Write();
    delete fout;
}
