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
    
    inf.readInt(1, 30, "n");
    inf.readSpace();
    inf.readInt(1, 10, "n");
    inf.readEoln();

    inf.readEof();
    return 0;
}
