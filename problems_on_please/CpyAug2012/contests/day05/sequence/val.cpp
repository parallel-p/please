/**
 * Validates that the first line contains the integer between 1 and 10^5, inclusive.
 * The second line should contains space-separated sequence of integers between -10^15 and 10^15, inclusive.
 * Also validates that file ends with EOLN and EOF.
 */

#include "testlib.h"

using namespace std;

int main()
{
    registerValidation();
    
    int n = inf.readInt(1, 1000, "n");
    inf.readEoln();

    for (int i = 0; i < n; i++)
    {
        inf.readInt(1, 2000000000);

        if (i + 1 < n)
            inf.readSpace();
    }
    inf.readEoln();

    inf.readEof();
    return 0;
}
