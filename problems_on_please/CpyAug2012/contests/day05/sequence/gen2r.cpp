#include "testlib.h"
#include <iostream>
#include <assert.h>

using namespace std;

int main(int argc, char* argv[])
{
    registerGen(argc, argv);
    int n = atoi(argv[1]);
    int m = atoi(argv[2]);
    assert( m < 32 );
    for (int i = 0; i < n; ++i) {
        if (i) cout << " ";
        cout << (1 << rnd.next(1, m - 1));
    }
    cout << endl;

    return 0;
}
