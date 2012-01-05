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

struct SegmTree {
    vi a;
    int n;

    SegmTree(int _n) {
        for (n = 1; n < _n; n <<= 1);
        a = vi(2 * n, 0);
    }

    void change(int pos, int newval) {
        a[n + pos] = newval;
        for (int v = (n + pos) >> 1; v; v >>= 1) {
            a[v] = min(a[v << 1], a[(v << 1) + 1]);
        }
    }

    int get(int v, int l0, int r0, int l, int r) {
        if (l >= r0 || l0 >= r)
            return INF;
        if (l <= l0 && r0 <= r)
            return a[v]; 
        return min(get(v << 1, l0, (l0 + r0) >> 1, l, r),
                   get((v << 1) + 1, (l0 + r0) >> 1, r0, l, r));
    }
    int get(int l, int r) {
        return get(1, 0, n, l, r);
    }
};

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
        
        SegmTree s(n);

        int ans = 0;
        for (int i = 0; i < n; i++) {
            s.change(i, a[i] - a[0]);    
            int mnval = s.get(0, i + 1);
            ans = max(ans, a[i] - a[0] - mnval);
        }
        printf("%d\n", ans); 
    }   
    return 0;
}
