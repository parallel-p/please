#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <algorithm>
#include <cmath>
#include <cassert>
#include <cstring>
#include <string>
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
    const int MAXN = 10001;
    const int MAXLEN = 300;

    for (int t = 0; t < 2; t++) {
        int n = rand() % MAXN;
        printf("%d\n", n);
        for (int i = 0; i < n; i++) {
            int len = rand() % MAXLEN + 1;
            printf("%d", rand() % 9 + 1);
            for (int j = 0; j < len - 1; j++)
                printf("%d", rand() % 10);
            if (i < n - 1)
                printf(" ");
        }
        printf("\n");
    }
    return 0;
}
