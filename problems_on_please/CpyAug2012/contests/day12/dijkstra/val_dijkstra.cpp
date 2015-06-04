#include "testlib.h"

using namespace std;

int main()
{
    registerValidation();
    
    int n = inf.readInt(1, 2000);
    inf.readSpace();
    int s = inf.readInt(1, n);
    inf.readSpace();
    int f = inf.readInt(1, n);
    inf.readEoln();
    int a;

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            a = inf.readInt(-1, 10000);
            if (i == j) {
                ensure(a == 0);
            }       
            if (j < n - 1) {
                inf.readSpace();
            }
        }
        inf.readEoln();
    }

    inf.readEof();
    return 0;
}