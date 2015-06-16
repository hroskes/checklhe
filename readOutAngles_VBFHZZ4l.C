void readOutAngles_VBFHZZ4l(TString filename)
{
    gROOT->LoadMacro("particletype.C+");
    gROOT->LoadMacro("momentum.C+");
    gROOT->LoadMacro("particle.C+");
    gROOT->LoadMacro("event.C+");
    gROOT->LoadMacro("lhefile.C+");

    LHEFile *fin = new LHEFile(filename);
    TFile *fout = TFile::Open(filename.ReplaceAll(".lhe", ".root"), "recreate");
    TTree *t = new TTree("SelectedTree", "SelectedTree");

    double mZZ, mZ1, mZ2;
    double costheta1_ZZ4l, costheta2_ZZ4l, Phi_ZZ4l, costhetastar_ZZ4l, Phi1_ZZ4l;
    vector<double> jetpt, jeteta, jetphi, jetmass;
    double costheta1_VBF, costheta2_VBF, Phi_VBF, costhetastar_VBF, Phi1_VBF, phistar_VBF, q2v1_VBF, q2v2_VBF;
    double mJJ, dEta, dPhi, dR;

    t->Branch("ZZMass", &mZZ, "ZZMass/D");
    t->Branch("Z1Mass", &mZ1, "Z1Mass/D");
    t->Branch("Z2Mass", &mZ2, "Z2Mass/D");

    t->Branch("costheta1_ZZ4l", &costheta1_ZZ4l, "costheta1_ZZ4l/D");
    t->Branch("costheta2_ZZ4l", &costheta2_ZZ4l, "costheta2_ZZ4l/D");
    t->Branch("Phi_ZZ4l", &Phi_ZZ4l, "Phi_ZZ4l/D");
    t->Branch("costhetastar_ZZ4l", &costhetastar_ZZ4l, "costhetastar_ZZ4l/D");
    t->Branch("Phi1_ZZ4l", &Phi1_ZZ4l, "Phi1_ZZ4l/D");

    t->Branch("JetPt", &jetpt);
    t->Branch("JetEta", &jeteta);
    t->Branch("JetPhi", &jetphi);
    t->Branch("JetMass", &jetmass);

    t->Branch("costheta1_VBF", &costheta1_VBF, "costheta1_VBF/D");
    t->Branch("costheta2_VBF", &costheta2_VBF, "costheta2_VBF/D");
    t->Branch("Phi_VBF", &Phi_VBF, "Phi_VBF/D");
    t->Branch("costhetastar_VBF", &costhetastar_VBF, "costhetastar_VBF/D");
    t->Branch("Phi1_VBF", &Phi1_VBF, "Phi1_VBF/D");
    t->Branch("q2v1_VBF", &q2v1_VBF, "q2v1_VBF/D");
    t->Branch("q2v2_VBF", &q2v2_VBF, "q2v2_VBF/D");

    t->Branch("mJJ", &mJJ, "mJJ/D");
    t->Branch("dEta", &dEta, "dEta/D");
    t->Branch("dPhi", &dPhi, "dPhi/D");
    t->Branch("dR", &dR, "dR/D");

    Event *ev;
    int i = 0;
    while (ev = fin->readevent())
    {
        i++;
        if (i % 10000 == 0)
            cout << "Converting event " << i << endl;
        ev->getZZmasses(mZZ, mZ1, mZ2);
        ev->getZZ4langles(costheta1_ZZ4l, costheta2_ZZ4l, Phi_ZZ4l, costhetastar_ZZ4l, Phi1_ZZ4l);
        ev->getjetmomenta(jetpt, jeteta, jetphi, jetmass);
        ev->getVBFangles(costheta1_VBF, costheta2_VBF, Phi_VBF, costhetastar_VBF, Phi1_VBF, q2v1_VBF, q2v2_VBF, false);
        ev->getVBFjetvariables(mJJ, dEta, dPhi, dR);
        t->Fill();
    }
    cout << "Total events converted: " << i << endl;
    delete fin;
    t->Write();
    delete fout;
}
