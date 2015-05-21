#include "TString.h"
#include <fstream>
#include "event.h"

class LHEFile
{
    private:
        TString _filename;
        ifstream _f;
        int _linenumber;
        TString _line;
        Event *_ev;
        bool _eof;
    public:
        LHEFile(TString filename);
        TString nextline();
        Event *readevent();
};
