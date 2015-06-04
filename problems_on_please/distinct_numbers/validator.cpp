#include "testlib.h"
#include <iostream>

using namespace std;

const int MAXN = 500000;
const int MAXV = 1000000000;

int main() {
    registerValidation();
    int n = inf.readInt(1, MAXN, "n");
    inf.readEoln();
    for (int i = 0; i < n; i++)
        inf.readInt(-MAXV, MAXV), inf.readSpace();
    inf.readEoln();
    inf.readEof();
    return 0;
}
