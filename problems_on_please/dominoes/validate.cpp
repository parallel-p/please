#include <utility>
#include <set>
#include "testlib.h"

using namespace std;

enum {
    N_MIN = 1,
    N_MAX = 100,
    A_MIN = -1000,
    A_MAX = +1000
};

int
main()
{
    registerValidation();
    
    int n = inf.readInt(N_MIN, N_MAX);
    inf.readSpace();
    int m = inf.readInt(N_MIN, N_MAX);
    inf.readSpace();
    int a = inf.readInt(A_MIN, A_MAX);
    inf.readSpace();
    int b = inf.readInt(A_MIN, A_MAX);
    inf.readEoln();
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            char c = inf.readChar();
            ensure(c == '.' || c == '*');
        }
        inf.readEoln();
    }
    inf.readEof();

    return 0;
}
