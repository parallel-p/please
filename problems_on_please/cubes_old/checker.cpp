#define EJUDGE
#include "testlib.h"

int main(int argc, char * argv[])
{
    registerTestlibCmd(argc, argv);
    int ainter = ans.readInt();
    int ointer = ouf.readInt();
    int ta, to;
    if(ainter != ointer)
        quitf(_wa, "expected %d intersects, found %d", ainter, ointer);
    for(int i = 0; i < ainter; i++)
    {
        ta = ans.readInt();
        to = ouf.readInt();
        if(ta != to)
            quitf(_wa, "expected %d color, found %d", ta, to);
    }
    ainter = ans.readInt();
    ointer = ouf.readInt();
    if(ainter != ointer)
        quitf(_wa, "expected %d (Masha), found %d", ainter, ointer);
    for(int i = 0; i < ainter; i++)
    {
        ta = ans.readInt();
        to = ouf.readInt();
        if(ta != to)
            quitf(_wa, "expected %d color, found %d", ta, to);
    }
    ainter = ans.readInt();
    ointer = ouf.readInt();
    if(ainter != ointer)
        quitf(_wa, "expected %d (Pasha), found %d", ainter, ointer);
    for(int i = 0; i < ainter; i++)
    {
        ta = ans.readInt();
        to = ouf.readInt();
        if(ta != to)
            quitf(_wa, "expected %d color, found %d", ta, to);
    }
    quitf(_ok, "ok");
}

