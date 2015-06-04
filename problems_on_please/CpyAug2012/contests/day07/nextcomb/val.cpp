#include "testlib.h"

using namespace std;

int main()
{
    registerValidation();
    
    int n = inf.readInt(1, 50, "n");
    inf.readSpace();
    int k = inf.readInt(1, 50, "k");
    inf.readEoln();
    int last = 0;
    for (int i = 0; i < k; ++i) {
        last = inf.readInt(last + 1, n, "a[i]");
        if (i + 1 < k) inf.readSpace();
    }
    inf.readEoln();
    inf.readEof();

    return 0;
}
