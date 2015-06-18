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

    double mZZ, mZ1, mZ2;
    double pTH, etaH, phiH;
    double pTHJJ, etaHJJ, phiHJJ, mHJJ;
    double costheta1_ZZ4l, costheta2_ZZ4l, Phi_ZZ4l, costhetastar_ZZ4l, Phi1_ZZ4l;
    vector<double> jetpt, jeteta, jetphi, jetmass;
    double costheta1_VBF, costheta2_VBF, Phi_VBF, costhetastar_VBF, Phi1_VBF, phistar_VBF, q2v1_VBF, q2v2_VBF;
    double mJJ, dEta, dPhi, dR;
    for (int i = 0; i < 3; i++)
    {
        t[i]->Branch("ZZMass", &mZZ, "ZZMass/D");
        t[i]->Branch("Z1Mass", &mZ1, "Z1Mass/D");
        t[i]->Branch("Z2Mass", &mZ2, "Z2Mass/D");

        t[i]->Branch("pTH", &pTH, "pTH/D");
        t[i]->Branch("etaH", &etaH, "etaH/D");
        t[i]->Branch("phiH", &phiH, "phiH/D");

        t[i]->Branch("mHJJ", &mHJJ, "mHJJ/D");
        t[i]->Branch("pTHJJ", &pTHJJ, "pTHJJ/D");
        t[i]->Branch("etaHJJ", &etaHJJ, "etaHJJ/D");
        t[i]->Branch("phiHJJ", &phiHJJ, "phiHJJ/D");

        t[i]->Branch("costheta1_ZZ4l", &costheta1_ZZ4l, "costheta1_ZZ4l/D");
        t[i]->Branch("costheta2_ZZ4l", &costheta2_ZZ4l, "costheta2_ZZ4l/D");
        t[i]->Branch("Phi_ZZ4l", &Phi_ZZ4l, "Phi_ZZ4l/D");
        t[i]->Branch("costhetastar_ZZ4l", &costhetastar_ZZ4l, "costhetastar_ZZ4l/D");
        t[i]->Branch("Phi1_ZZ4l", &Phi1_ZZ4l, "Phi1_ZZ4l/D");

        t[i]->Branch("JetPt", &jetpt);
        t[i]->Branch("JetEta", &jeteta);
        t[i]->Branch("JetPhi", &jetphi);
        t[i]->Branch("JetMass", &jetmass);

        t[i]->Branch("costheta1_VBF", &costheta1_VBF, "costheta1_VBF/D");
        t[i]->Branch("costheta2_VBF", &costheta2_VBF, "costheta2_VBF/D");
        t[i]->Branch("Phi_VBF", &Phi_VBF, "Phi_VBF/D");
        t[i]->Branch("costhetastar_VBF", &costhetastar_VBF, "costhetastar_VBF/D");
        t[i]->Branch("Phi1_VBF", &Phi1_VBF, "Phi1_VBF/D");
        t[i]->Branch("q2v1_VBF", &q2v1_VBF, "q2v1_VBF/D");
        t[i]->Branch("q2v2_VBF", &q2v2_VBF, "q2v2_VBF/D");

        t[i]->Branch("mJJ", &mJJ, "mJJ/D");
        t[i]->Branch("dEta", &dEta, "dEta/D");
        t[i]->Branch("dPhi", &dPhi, "dPhi/D");
        t[i]->Branch("dR", &dR, "dR/D");
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
        ev->getHmomentum(pTH, etaH, phiH);
        ev->getHJJmomentum(pTHJJ, etaHJJ, phiHJJ, mHJJ);
        ev->getZZ4langles(costheta1_ZZ4l, costheta2_ZZ4l, Phi_ZZ4l, costhetastar_ZZ4l, Phi1_ZZ4l);
        ev->getjetmomenta(jetpt, jeteta, jetphi, jetmass);
        ev->getVBFangles(costheta1_VBF, costheta2_VBF, Phi_VBF, costhetastar_VBF, Phi1_VBF, q2v1_VBF, q2v2_VBF, false);
        ev->getVBFjetvariables(mJJ, dEta, dPhi, dR);
        t[j]->Fill();
    }
    cout << "Total events converted: " << i << endl;
    delete fin;
    for (int i = 0; i < 3; i++)
    {
        fout[i]->cd();
        t[i]->Write();
        delete fout[i];
    }
}
