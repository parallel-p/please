#include "testlib.h"

using namespace std;

int main()
{
    registerValidation();
    int n, k, *counts;
    n = inf.readInt(1, 100000);
    inf.readEoln();
    counts = new int [n];

    for (int i = 0; i < n; ++i) {
        counts[i] = 0;
    }      
    for (int i = 0; i < n; ++i) {
        k = inf.readInt(1, n);
        if (i < n - 1) {
            inf.readSpace();
        }
        ++counts[k - 1];
    }
    inf.readEoln();
    inf.readEof();

    for (int i = 0; i < n; ++i) {
        ensure(counts[i] == 1);
    }

    delete[] counts;
    return 0;
}