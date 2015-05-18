#include "TTree.h"
#include <vector>
#include <map>
using namespace std;

class Tree : public TTree
{
    private:
        vector<Int_t*> ints;
        vector<Float_t*> floats;
        vector<Double_t*> doubles;
        map<TString, pair<char, unsigned int>> branchesmap;
    public:
        TBranch *Branch(TString name, char type);
        TBranch *EnsureBranch(TString name, char type);
        
}
