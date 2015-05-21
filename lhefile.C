#include "lhefile.h"
#include "event.C"

LHEFile::LHEFile(TString filename) : _filename(filename), _f(filename), _linenumber(0), _line(""), _ev(0)
{}

TString LHEFile::nextline()
{
    std::string line;
    if (std::getline(_f, line))
        _line = line;
    else
        _line = "";
    _linenumber++;
    return _line;
}

Event *LHEFile::readevent()
{
    delete _ev;
    while (! nextline().Contains("<event>"))
    {
        if (!_line)
            return 0;
        if (_line.Contains("</event>"))
            throw std::runtime_error((TString("Extra </event>! ") += _linenumber).Data());
    }
    _ev = new Event(_linenumber);

    TString firstline = nextline();
    int nparticles = 0;
    if (nPart(1, firstline).IsDigit())
        nparticles = nPart(0, firstline).Atoi();
    else
        throw std::runtime_error((TString("First line of the event does not start with an integer! ") += _linenumber).Data());

    for (int i = 0; i < nparticles && ! nextline().Contains("</event>"); i++)
    {
        if (!_line)
            throw std::runtime_error("File ends in the middle of an event!");
        if (_line.Contains("<event>"))
            throw std::runtime_error((TString("Extra </event>! ") += _linenumber).Data());
        _ev->particle(_line);
    }

    while (! nextline().Contains("</event>"))
    {}

    _ev->finished();
    return _ev;
}
