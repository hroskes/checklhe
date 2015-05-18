#include "helperfunctions.h"

TString nPart(int part, TString string, TString delimit, bool multipleasone, bool removerest)
{
    if (part <= 0) return "";
    for (int i = 0; i < part; i++)    //part-1 times
    {
        if (multipleasone && string.BeginsWith(delimit))
            i--;
        if (string.Index(delimit) < 0) return "";
        string.Replace(0,string.Index(delimit)+1,"",0);
    }
    while (multipleasone && string.BeginsWith(delimit))
        string.Replace(0,string.Index(delimit)+1,"",0);

    if (string.Index(delimit) >= 0 && removerest)
        string.Remove(string.Index(delimit));
    return string;
}
