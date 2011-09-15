//----------------------------------------------------------------------------
/** @file SgProcess.h */
//----------------------------------------------------------------------------

#ifndef SG_PROCESS_H
#define SG_PROCESS_H

// Not yet implemented for Windows
#ifndef WIN32

#include <ext/stdio_filebuf.h> // GCC specific
#include <iosfwd>
#include <memory>

//----------------------------------------------------------------------------

/** Run a child process and provide access to its standard input and output
    streams.
    The implementation of this class is platform-dependent. Currently, only
    POSIX systems are supported (it also uses GCC-specific extensions to
    open C++ streams from file descriptors). */
class SgProcess
{
public:
    /** Constructor.
        @throws SgException on failure */
    SgProcess(const std::string& command);

    ~SgProcess();

    std::istream& Input();

    std::ostream& Output();

private:
    std::auto_ptr<__gnu_cxx::stdio_filebuf<char> > m_bufIn;

    std::auto_ptr<__gnu_cxx::stdio_filebuf<char> > m_bufOut;

    std::auto_ptr<std::istream> m_in;

    std::auto_ptr<std::ostream> m_out;
};

inline std::istream& SgProcess::Input()
{
    return *m_in;
}

inline std::ostream& SgProcess::Output()
{
    return *m_out;
}

//----------------------------------------------------------------------------

#endif // ifndef WIN32

#endif // SG_PROCESS_H
