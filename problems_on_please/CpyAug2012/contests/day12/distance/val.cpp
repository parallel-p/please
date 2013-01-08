#include "testlib.h"

using namespace std;

int main()
{
    registerValidation();
    
    int n = inf.readInt(1, 5000, "n");
    inf.readSpace();
    int m = inf.readInt(1, 100000, "m");
    inf.readEoln();
    int s = inf.readInt(1, n, "m");
    inf.readSpace();
    int f = inf.readInt(1, n, "m");
    ensure(s != f);
    inf.readEoln();

    for (int i = 0; i < m; i++) {
        inf.readInt(1, n, "");
        inf.readSpace();
        inf.readInt(1, n, "");
        inf.readSpace();
        inf.readInt(1, 100000, "");
        inf.readEoln();
    }

    inf.readEof();
    return 0;
}
