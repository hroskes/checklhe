#include "readOutAngles_VBFHZZ4l_splitflavors.C"
void test()
{
    readOutAngles_VBFHZZ4l_splitflavors("VBFscalar33_decayed_small.lhe");
    TFile::Open("VBFscalar33_decayed_small_2e2mu.root");
    double costhetastar=0, Phi1=0;
    //SelectedTree->SetBranchAddress("costheta1_VBF", &costhetastar);
    SelectedTree->SetBranchAddress("costhetastar_VBF", &costhetastar);
    SelectedTree->SetBranchAddress("Phi1_VBF", &Phi1);
    for (int i = 0; i < SelectedTree->GetEntries(); i++)
    {
        SelectedTree->GetEntry(i);
        cout << i << "    " << costhetastar << "    " << Phi1 << endl;
    }
}
