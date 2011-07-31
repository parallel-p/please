#include "testlib.h"
#include <iostream>
#include <cstdlib>

using namespace std;

const int MAXV = 1000000000;

int main(int argc, char* argv[])
{
    registerGen(argc, argv);

    int n = atoi(argv[1]);
    cout << n << endl;
    for (int i = 0; i < n; i++)
        cout << rnd.next(-MAXV, MAXV) << ' ';
    cout << endl;
    return 0;
}
