#define _CRT_SECURE_NO_WARNINGS

#include <string>
#include <vector>
#include <cmath>
#include <map>
#include <algorithm>
#include <set>
#include <iostream>
#include <sstream>
#include <cstdio>
#include <cassert>
#include <utility>

using namespace std;

#define EPS 1E-8

#define forn(i, n) for (int i = 0; i < int(n); i++)
#define forv(i, a) for (int i = 0; i < int(a.size()); i++)
#define fors(i, a) for (int i = 0; i < int(a.length()); i++)
#define all(a) a.begin(), a.end()
#define pb push_back
#define mp make_pair
#define VI vector<int>
#define VS vector<string>

#define norm(a) sort(all(a)); a.erase(unique(all(a)), a.end());
#define num(a, v) (int)(lower_bound(all(a), v) - a.begin())

#define C_IN_FILE "tshirts.in"
#define C_OUT_FILE "tshirts.out"

vector< vector<long long> > d;
long long ans;
int n;
vector<int> s;
long long mod = 1000000000LL;

void outdata() {
	cout << ans << endl;
}

long long calc(int l, int r) {
	long long& res = d[l][r];
	if (res != -1) {
		return res;
	}
	if (l == r) {
		return res = 2;
	}
	if (l > r) {
		return res = 1;
	}
	res = calc(l + 1, r) + calc(l, r - 1);
	if (s[l] != s[r]) res -= calc(l + 1, r - 1);
	res = (res % mod + mod) % mod;
	return res;
}

void solve() {
	d.resize(s.size(), vector<long long>(s.size(), -1));
	ans = calc(0, s.size() - 1) - 1;
	ans = (ans % mod + mod) % mod;
}

void readdata() {
	cin >> n;
	s.resize(n);
	assert(0 < s.size() && s.size() <= 2000);
	forv(i, s) {
		cin >> s[i];
		assert(1 <= s[i] && s[i] <= 1000000000);
	}
}

int main() {
    freopen(C_IN_FILE, "rt", stdin);
    freopen(C_OUT_FILE, "wt", stdout);
	
	readdata();
	solve();
	outdata();
	return 0;
}
