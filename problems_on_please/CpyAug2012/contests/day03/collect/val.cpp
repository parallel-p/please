#include "testlib.h"

using namespace std;

int main()
{
    registerValidation();
    
    int n, k;
    inf.readInt(1, 2000000000);
    for (int i = 0; i < n-1; i++)
    {
        inf.readSpace();
        inf.readInt(1, 2000000000);
    }
    inf.readEoln();

    inf.readInt(1, 2000000000);
    for (int i=0; i<k-1; i++)
    {
        inf.readSpace();
        inf.readInt(1, 2000000000);
    }
    inf.readEoln();

    inf.readEof();
    return 0;
}
