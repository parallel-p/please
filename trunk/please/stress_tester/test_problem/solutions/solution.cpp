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
    while(scanf("%d%d", &a, &b) >= 1) {
        printf("%d\n", a + b);
    }
    return 0;
}
