#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <cstring>
#include <algorithm>
#include <cmath>
#include <cassert>
#include <ctime>
#include <vector>
#include <string>

using namespace std;

typedef vector<int> vi;

#define TASKNAME "inside"
#define EPS (1e-9)
#define INF ((int)1e9)
#define mp make_pair
#define pb push_back

const int maxs = 301;
char s[maxs];

struct Bigint {
    vi a;

    Bigint() {a.clear();}
    Bigint(int n) {
        a.clear();
        while(n) {
            a.pb(n % 10);
            n /= 10;
        }
    }

    void read() {
        scanf("%s", s);
        int n = strlen(s);
    
        char *q = s;
        while(q[0] == '0') {
            q++;
            n--;
            continue;
        }

        a = vi(n, 0);
        
        for (int i = 0; i < n; i++) {
            a[n - i - 1] = s[i] - '0';    
        }
    }

    void write() {
        if (!a.size()) {
            printf("0");
            return;
        }

        for (int i = (int)a.size() - 1; i >= 0; i--) {
            printf("%d", a[i]);    
        }
    }

    void writeln() {
        write();
        printf("\n");
    }
};

inline int cmp(const Bigint &a, const Bigint &b) {
    if (a.a.size() != b.a.size())
        return a.a.size() < b.a.size() ? -1 : 1;
    int n = a.a.size();
    assert(n == (int)b.a.size());
    for (int i = n - 1; i >= 0; i--) {
        if (a.a[i] < b.a[i])
            return -1;
        if (a.a[i] > b.a[i])
            return 1;
    }
    return 0;
}

inline bool operator < (const Bigint &a, const Bigint &b) {
    return cmp(a, b) < 0;
};

const int maxn = ((int)1e4);
Bigint a[maxn], b[maxn];

int main() { 
    freopen(TASKNAME".in", "r", stdin);
    freopen(TASKNAME".out", "w", stdout);
    int n;
    scanf("%d", &n);
    for (int i = 0; i < n; i++) {
        a[i].read();              
    }
    sort(a, a + n);

    int m;
    scanf("%d", &m);
    for (int i = 0; i < m; i++) {
        b[i].read();              
    }
    sort(b, b + m);
    
    int ans = 0;
    int i = 0;
    for (int j = 0; j < m; j++) {
        int cmpl = 2;
        while(i < n) {
            cmpl = cmp(a[i], b[j]);    
            if (cmpl >= 0)
                break;
            i++;
        }

        if (!cmpl)
            ans++;
    }
    
    printf("%d\n", ans);
    return 0;
}
