#include "testlib.h"

using namespace std;

const int MAXN = 500000;
const int MAXV = 1000000000;

int main() {
    registerValidation();
    int n = inf.readInt(1, MAXN, "n");
    inf.readEoln();
    for (int i = 0; i < n - 1; i++)
        inf.readInt(-MAXV, MAXV), inf.readSpace();
    inf.readInt(-MAXV, MAXV);
    inf.readEoln();
    return 0;
}
