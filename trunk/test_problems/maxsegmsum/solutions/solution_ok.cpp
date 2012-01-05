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

ll rdtsc() {
    ll tmp;
    asm("rdtsc" : "=A"(tmp));
    return tmp;
}

#define TASKNAME "sum"
#define pb push_back
#define mp make_pair
#define EPS (1e-9)
#define INF ((int)1e9)
#define sqr(x) ((x) * (x))         

int main() {
    srand(rdtsc());
    freopen(TASKNAME".in", "r", stdin);
    freopen(TASKNAME".out", "w", stdout);

    int n;
    while (scanf("%d", &n) >= 1) {
        vi a(n);
        for (int i = 0; i < n; i++) {
            assert(scanf("%d", &a[i]));
        }
        
        vi b(--n);
        for (int i = 0; i < n; i++)
            b[i] = a[i + 1] - a[i];
        
        int lastans = -1, ans = 0;
        for (int i = 0; i < n; i++) {
            lastans = max(0, lastans);
            lastans += b[i];
            
            if (ans < lastans)
                ans = lastans;
        }

        printf("%d\n", ans); 
    }   
    return 0;
}
