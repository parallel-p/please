#include "testlib.h"

using namespace std;

int main()
{
    registerValidation();
    
    int n = inf.readInt(1, 100, "n");
    inf.readEoln();

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            int x = inf.readInt(-100, 100, "");

            if (i == j) {
                ensure(x == 0);
            }
            if (j + 1 < n)
                inf.readSpace();
        }
        inf.readEoln();
    }

    inf.readEof();
    return 0;
}
