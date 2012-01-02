#include <cstdio>
#include <cstdlib>
#include <algorithm>
#include <cmath>
#include <cstring>
#include <string>
#include <iostream>
#include <cassert>
#include <vector>

using namespace std;

typedef long long ll;
ll rdtsc() {
    ll tmp;
    asm("rdtsc" : "=A"(tmp));
    return tmp;
}

int main() {
    srand(rdtsc());
    const int max_test = 100;
    //for (int t = 0; t < max_test; t++) {
        int a = rand() % 2323, b = rand() % 2323;
        printf("%d %d ", a, b);
    //}
}
