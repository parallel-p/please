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

int main(int argc, char * const argv[]) {
    if (argc != 4)
        exit(239);
    
    printf(argv[2]);
    freopen(argv[2], "r", stdin);
    int answer;
    if (!scanf("%d", &answer)) {
        printf("PE!\n");
        assert(251);
    }
    freopen(argv[3], "r", stdin);
    int correct_answer;
    if (!scanf("%d", &correct_answer)) {
        printf("PE!\n");
        assert(251);
    }
    if (correct_answer != answer)
        printf("WA!\n"), exit(1);
    printf("OK! :)\n");        
    return 0;    
}
