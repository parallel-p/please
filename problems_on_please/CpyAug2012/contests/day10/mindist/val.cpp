#include "testlib.h"

using namespace std;

int main()
{
    registerValidation();

    int n = inf.readInt(1, 100);
    inf.readEoln();

    int s[100][100];

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            s[i][j] = inf.readInt(0, 1);

            if (j < n - 1) {
                inf.readSpace();
            } else {
                inf.readEoln();
            }
        }
    }

    inf.readEof();

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (i == j) {
                ensure(s[i][j] == 0);
            } else {
                ensure(s[i][j] == s[j][i]);
            }
        }
    }

    return 0;
}
