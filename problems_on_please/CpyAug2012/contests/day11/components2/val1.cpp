#include "testlib.h"

/* 
	Checks if first line contains exactly one integer n (1 <= n <= 1000)
	and next n lines contain exactly two positive integer numbers not greater than 100000
	separated by single space
*/
using namespace std;

int main()
{
    registerValidation();
    
    int n = inf.readInt(1, 100000);
    inf.readSpace();

    int m = inf.readInt(0, 100000);
    inf.readEoln();


    for (int i = 0; i < m; i++)
    {
        inf.readInt(1, n);
        inf.readSpace();
        inf.readInt(1, n);
        inf.readEoln();
    }

    inf.readEof();
    return 0;
}
