/**
 * Validates that the first line contains two integer n, m between 1 and 10^3, inclusive.
 * Next n lines contain space-separated sequence of integers between 0 and 1, inclusive.
 * Also validates that file ends with EOLN and EOF.
 */

#include "testlib.h"

using namespace std;

const int MAXN = 1000;
int main() {
    registerValidation();
    
    int n = inf.readInt(1, MAXN, "n");
    inf.readSpace();    
    int m = inf.readInt(1, MAXN, "m");
    inf.readEoln();

    for (int i = 0; i < n; ++i) {
        for (int j= 0; j < m; ++j) {
            inf.readInt(0, 1, "number");
            if (j + 1 < m)
                inf.readSpace();
        }
    	inf.readEoln();
    }
    
    inf.readEof();
    return 0;
}
