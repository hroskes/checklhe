#ifndef tree_C
#define tree_C

#include "tree.h"
#include <assert.h>

TBranch *Tree::Branch(TString name, char type)
{
    pair<char, int> branch = branchesmap[name];
    if (branch != branchesmap.end())
        if (type == branch.first)
           return FindBranch(name);
        else
        {
           cout << "A branch of name " << name << " already exists with different type!" << endl;
           assert(0);
           return 0;
        }
    switch (type)
    {
        case 'I':
            int *i = new int();
            ints.push_back(i);
            branchesmap[name] = make_pair('I',ints.size()-1);
            return TTree::Branch(name, i, name + "/I");
        case 'F':
            float *f = new float();
            floats.push_back(f);
            branchesmap[name] = make_pair('F',floats.size()-1);
            return TTree::Branch(name, f, name + "/F");
        case 'D':
            double *d = new double();
            doubles.push_back(d);
            branchesmap[name] = make_pair('D',doubles.size()-1);
            return TTree::Branch(name, d, name + "/D");
        default:
            assert(0);
            return 0;
    }
}
#endif
