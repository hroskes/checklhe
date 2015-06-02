void test()
{
    TFile::Open("VBFscalar33_decayed_small_2e2mu.root");
    double costhetastar=0, Phi1=0;
    SelectedTree->SetBranchAddress("costheta1_VBF", &costhetastar);
    SelectedTree->SetBranchAddress("costheta2_VBF", &Phi1);
    for (int i = 0; i < SelectedTree->GetEntries(); i++)
    {
        SelectedTree->GetEntry(i);
        cout << i << "    " << costhetastar << "    " << Phi1 << endl;
    }
}
