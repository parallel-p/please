#include "testlib.h"
#include <iostream>

using namespace std;

int main() {
    registerValidation();
    int n = inf.readInt(1, (int)1e5);
    inf.readEoln();
    for (int i = 0; i < n; i++) {
        inf.readInt(1, (int)1e9);
        if (i < n - 1)
            inf.readChar(' ');
        else
            inf.readEoln();
    }
    inf.readEof();
    return 0;
}
