#include "testlib.h"
#include <iostream>
#include <algorithm>
#include <functional>
#include <vector>

using namespace std;

int main(int argc, char** argv) {
    registerGen(argc, argv);

    int n = atoi(argv[1]);
    int m = atoi(argv[2]);
    cout << n << " " << m << endl;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            if (j) cout << " ";
            cout << rnd.next(2, 250);
        }
        cout << endl;
    }
    return 0;
}
