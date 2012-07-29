// 0-1-2 graphs

#define _CRT_SECURE_NO_DEPRECATE

#include <algorithm>
#include <iostream>
#include <cassert>
#include <vector>
#include <cstdio>
#include <cstdlib>
#include <cstring>

using namespace std;

const int nmax = 300001;
const int inf = (int)1e+9;

int n, m, k;
int mark[nmax];
int a[nmax];
int way[nmax];
int q[2*nmax];
vector < int > d[nmax];

void init() {
    scanf("%d%d", &n, &m);
    for (int i = 0; i < n; ++i) {
        scanf("%d", &mark[i]);
        assert(mark[i] >= 1 && mark[i] <= 2);
    }
    int x, y;
    for (int i = 0; i < m; ++i) {
        scanf("%d%d", &x, &y);
        d[x - 1].push_back(y - 1);
        d[y - 1].push_back(x - 1);
        assert(x >= 1 && x <= n && y >= 1 && y <= n && x != y);
    }

    k = n;
    for (int i = 1; i < n; i += 2) {
        for (int j = 0; j < (int)d[i].size(); ++j) {
            y = d[i][j];
            if (mark[i] != mark[y]) {
                d[i][j] = k;
                d[k].push_back(y);
                k++;
            }
        }
    }
}

void solve() {
    memset(way, -1, sizeof(way));
    int l = nmax, r = l + 1, x, y;
    q[0] = 0;
    a[0] = 0;
    for (int i = 1; i < k; ++i) a[i] = inf;
    while (l < r) {
        x = q[l];
        for (int j = 0; j < (int)d[x].size(); ++j) {
            y = d[x][j];
            if (mark[x] == mark[y] && a[y] > a[x]) {
                q[l--] = y;
                a[y] = a[x];
                way[y] = x;                
            } else if (a[y] > a[x] + 1) {
                q[r++] = y;
                a[y] = a[x] + 1;
                way[y] = x;
            }
        }
        l++;
    }
}

void writeanswer() {
    if (a[n - 1] == inf) printf("impossible");
    else {
        vector < int > ans;
        ans.reserve(n);
        int x = n - 1;
        while (x != -1) {
            if (x < n) ans.push_back(x);
            x = way[x];
        }
        printf("%d %d\n", a[n - 1], (int)ans.size());
        for (int i = (int)ans.size() - 1; i >= 0; --i) {
            printf("%d", ans[i] + 1);
            if (i > 0) printf(" ");
        }
    }
}

int main() {
    freopen("island2.in", "rt", stdin);
    freopen("island2.out", "wt", stdout);

    init();
    solve();
    writeanswer();   

    return 0;
}
