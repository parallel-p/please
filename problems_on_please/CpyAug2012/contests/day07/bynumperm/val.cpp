#include "testlib.h"

using namespace std;

int main()
{
    registerValidation();
    
    int n = inf.readInt(1, 12, "n");
    inf.readEoln();
    int fact = 1;
    for (int i = 1; i <= n; ++i) {
        fact *= i;
    }
    inf.readInt(0, fact - 1, "fact");
    inf.readEoln();
    inf.readEof();

    return 0;
}
