void readOutAngles_VBFHZZ4l_splitflavors(TString filename)
{
    gROOT->LoadMacro("particletype.C+");
    gROOT->LoadMacro("momentum.C+");
    gROOT->LoadMacro("particle.C+");
    gROOT->LoadMacro("event.C+");
    gROOT->LoadMacro("lhefile.C+");

    LHEFile *fin = new LHEFile(filename);
    TFile *fout[3] = {0, 0, 0};
    TTree *t[3] = {0, 0, 0};
    fout[0] = TFile::Open(TString(filename).ReplaceAll(".lhe", "_4e.root"), "recreate");
    t[0] = new TTree("SelectedTree", "SelectedTree");
    fout[1] = TFile::Open(TString(filename).ReplaceAll(".lhe", "_4mu.root"), "recreate");
    t[1] = new TTree("SelectedTree", "SelectedTree");
    fout[2] = TFile::Open(TString(filename).ReplaceAll(".lhe", "_2e2mu.root"), "recreate");
    t[2] = new TTree("SelectedTree", "SelectedTree");

    double mZZ, mZ1, mZ2, costheta1, costheta2, Phi, costhetastar, Phi1;
    vector<double> jetpt, jeteta, jetphi, jetmass;
    for (int i = 0; i < 3; i++)
    {
        t[i]->Branch("ZZMass", &mZZ, "ZZMass/D");
        t[i]->Branch("Z1Mass", &mZ1, "Z1Mass/D");
        t[i]->Branch("Z2Mass", &mZ2, "Z2Mass/D");
        t[i]->Branch("costheta1", &costheta1, "costheta1/D");
        t[i]->Branch("costheta2", &costheta2, "costheta2/D");
        t[i]->Branch("Phi", &Phi, "Phi/D");
        t[i]->Branch("costhetastar", &costhetastar, "costhetastar/D");
        t[i]->Branch("Phi1", &Phi1, "Phi1/D");
        t[i]->Branch("JetPt", &jetpt);
        t[i]->Branch("JetEta", &jeteta);
        t[i]->Branch("JetPhi", &jetphi);
        t[i]->Branch("JetMass", &jetmass);
    }

    Event *ev;
    int i = 0;
    while (ev = fin->readevent())
    {
        i++;
        if (i % 10000 == 0)
            cout << "Converting event " << i << endl;
        int j = -999;
        switch (ev->getZZ4lflavor())
        {
            case 0: j = 0; break;
            case 1: j = 1; break;
            case 3: case 6: j = 2; break;
            default: continue;
        }
        ev->getZZmasses(mZZ, mZ1, mZ2);
        ev->getZZ4langles(costheta1, costheta2, Phi, costhetastar, Phi1);
        ev->getjetmomenta(jetpt, jeteta, jetphi, jetmass);
        t[j]->Fill();
    }
    cout << "Total events converted: " << i << endl;
    //delete fin;
    for (int i = 0; i < 3; i++)
    {
        fout[i]->cd();
        t[i]->Write();
        delete fout[i];
    }
}
