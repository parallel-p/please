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
#define INF ((int)1e9 + 1)
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
        
        vvi dyn(n, vi(n));
        int ans = 0;
        for (int len = 0; len < n; len++) {
            for (int i = 0; i < n - len; i++) {
                int &cur = dyn[len][i];
                if (!len) {
                    cur = b[i];
                    ans = max(ans, cur);
                    continue;
                }

                cur = dyn[len - 1][i] + b[i + len];
                ans = max(ans, cur);
            }
        }
        printf("%d\n", ans); 
    }   
    return 0;
}
