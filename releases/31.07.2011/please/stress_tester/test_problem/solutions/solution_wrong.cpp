#include <iostream>
#include <cstring>
#include <cstdio>
#include <cstdlib>

using namespace std;

#define TASKNAME "aplusb"
int main (int argc, char * const argv[]) {
    freopen(TASKNAME".in", "r", stdin);
    freopen(TASKNAME".out", "w", stdout);
    int a, b;
    //scanf("%d%d", &a, &b);
    while(scanf("%d%d", &a, &b) >= 2) {
        if (a < 2000) {
        printf("%d\n", a + b);
        } else {
            printf("%d\n", a * b);
        }
    }
    //printf("%d\n", a + b);
    return 0;
}
