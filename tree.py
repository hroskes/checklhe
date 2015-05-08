import ROOT
import array

#https://root.cern.ch/root/html/TTree.html, Case A
#https://docs.python.org/2/library/array.html
#of course they had to use the opposite capital/lowercase conventions
#{Type for TTree: type for array}
typemap = {
           'B': 'b',
           'b': 'B',
           'S': 'h',
           's': 'H',
           'I': 'i',
           'i': 'I',
           'F': 'f',
           'D': 'd',
           'L': 'l',
           'l': 'L',
          }

class tree(ROOT.TTree):

    def __init__(self, *args, **kwargs):
        self.branches = {}
        self.setyet = {}
        super(tree, self).__init__(*args, **kwargs)

    def Branch(self, *args, **kwargs):
        if len(args) == 2 and len(kwargs) == 0:
            name = args[0]
            type = args[1]

            if type not in typemap:
                raise IndexError("The allowed types for tree are\n" + ", ".join(a for a in typemap) + "\n" + type + " is not allowed")
            self.branches[name] = array.array(typemap[type], [0])
            self.setyet[name] = False
            super(tree, self).Branch(name, self.branches[name], name + "/" + typemap[type])
        else:
            super(tree, self).Branch(*args, **kwargs)

    def __setitem__(self, name, value):
        if name in self.branches:
            self.branches[name][0] = value
            self.setyet[name] = True
        else:
            raise KeyError(name + " is not yet a branch in the tree!")
    def __getitem__(self, name):
        try:
            return self.branches[name][0]
        except KeyError:
            raise KeyError(name + " is not yet a branch in the tree!")

    def Fill(self, force = False):
        if not force:
            for name in self.setyet:
                if not self.setyet[name]:
                    raise RuntimeError("Warning: you have not yet set " + name + " but you are trying to fill the tree.\n" +
                                       "To turn off this check, run tree.Fill(force = True)")
        super(tree, self).Fill()
        for name in self.setyet:
            self.setyet[name] = False
