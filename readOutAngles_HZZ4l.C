void readOutAngles_HZZ4l(TString filename)
{
    gROOT->LoadMacro("particletype.C+");
    gROOT->LoadMacro("momentum.C+");
    gROOT->LoadMacro("particle.C+");
    gROOT->LoadMacro("event.C+");
    gROOT->LoadMacro("lhefile.C+");

    LHEFile *fin = new LHEFile(filename);
    TFile *fout = TFile::Open(filename.ReplaceAll(".lhe", ".root"), "recreate");
    TTree *t = new TTree("SelectedTree", "SelectedTree");

    double mZZ, mZ1, mZ2, costheta1, costheta2, Phi, costhetastar, Phi1;
    vector<double> jetpt, jeteta, jetphi, jetmass;
    t->Branch("ZZMass", &mZZ, "ZZMass/D");
    t->Branch("Z1Mass", &mZ1, "Z1Mass/D");
    t->Branch("Z2Mass", &mZ2, "Z2Mass/D");
    t->Branch("costheta1", &costheta1, "costheta1/D");
    t->Branch("costheta2", &costheta2, "costheta2/D");
    t->Branch("Phi", &Phi, "Phi/D");
    t->Branch("costhetastar", &costhetastar, "costhetastar/D");
    t->Branch("Phi1", &Phi1, "Phi1/D");
    t->Branch("JetPt", &jetpt);
    t->Branch("JetEta", &jeteta);
    t->Branch("JetPhi", &jetphi);
    t->Branch("JetMass", &jetmass);

    Event *ev;
    int i = 0;
    while (ev = fin->readevent())
    {
        i++;
        ev->getZZmasses(mZZ, mZ1, mZ2);
        ev->getZZ4langles(costheta1, costheta2, Phi, costhetastar, Phi1);
        ev->getjetmomenta(jetpt, jeteta, jetphi, jetmass);
        t->Fill();
        if (i % 10000 == 0)
            cout << "Converted " << i << " events" << endl;
    }
    cout << "Total events converted: " << i << endl;
    delete fin;
    t->Write();
    delete fout;
}
