#include "testlib.h"

using namespace std;

int main()
{
    registerValidation();
    int n, m;
    n = inf.readInt(0, 100000);
    inf.readChar(' ');
    m = inf.readInt(0, 100000);
    inf.nextLine();
    for(int i = 0; i < n; i++)
    {
        inf.readInt(0, 1000000000);
        inf.nextLine();
    }
    for(int i = 0; i < m; i++)
    {
        inf.readInt(0, 1000000000);
        inf.nextLine();
    }
    inf.readEoln();
    inf.readEof();

    return 0;
}

