#include "testlib.h"
#include <iostream>
#include <algorithm>
#include <functional>
#include <vector>

using namespace std;

enum {
MAXN = 300,
MAX = 10000
};

const bool comp(const int &a, const int &b) {
return a > b;
}

int main(int argc, char** argv) {
    registerGen(argc, argv);

    int n = rnd.next(1, MAXN);
    vector<int> a;
    for (int i = 0; i < n; ++i) {
        a.push_back(rnd.next(1, 20000));
    }
    cout << rnd.next(1, MAX) << endl;
    for (int i = 0; i < n; ++i) {
        if (!i) {
            cout << a[i];
        } else {
            cout << " " << a[i];
        }
    }
    cout << endl;
    return 0;
}
