#include "testlib.h"
#include <iostream>
#include <assert.h>

using namespace std;

int main(int argc, char* argv[])
{
    registerGen(argc, argv);
    int n = atoi(argv[1]);
    assert( n < 32 );
    for (int i = 0; i < n; ++i) {
        if (i) cout << " ";
        cout << (1 << i);
    }
    cout << endl;

    return 0;
}
