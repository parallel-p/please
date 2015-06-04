#include "testlib.h"
#include <vector>
#include <iostream>
#include <cmath>
#include <cstdlib>

using namespace std;

const int MAXV = 1000000000;

int main(int argc, char* argv[])
{
    registerGen(argc, argv);

    int n = atoi(argv[1]);
    int sqn = (int)sqrt((float)n);

    vector<int> V(sqn);
    for (int i = 0; i < sqn; i++)
        V[i] = rnd.next(-MAXV, MAXV);
    
    cout << n << endl;

    for (int i = 0; i < n; i++)
        cout << V[rnd.next(0, sqn - 1)] << ' ';
    cout << endl;
    return 0;
}
