#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <algorithm>
#include <iostream>
#include <cstring>
#include <vector>
#include <string>
#include <set>
#include <map>
#include <cassert>
#include <ctime>
#include "testlib.h"

using namespace std;

#ifdef WIN32
    #define LLD "%I64d"
#else
    #define LLD "%lld"
#endif

typedef pair<int, int> pii;
typedef long long ll;
typedef vector<int> vi;
typedef vector<vi> vvi;
typedef vector<bool> vb;
typedef vector<vb> vvb;
typedef vector<ll> vll;
typedef vector<vll> vvll;

#define pb push_back
#define mp make_pair
#define EPS (1e-9)
#define INF ((int)1e9)
#define sqr(x) ((x) * (x))         

void writeTest(int test)
{
    startTest(test);
    int n = (int)1e5;
    cout << n << endl;
    for (int i = 0; i < n; i++) {
        int x = rnd.next(1, (int)1e9);
        printf("%d%c", x, " \n"[i == n - 1]);
    }
}

int main(int argc, char* argv[])
{
    registerGen(argc, argv);

    for (int i = 1; i <= 8; i++)
        writeTest(i);
    
    return 0;
}
