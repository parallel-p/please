#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <algorithm>

using namespace std;

const int MAXN = 1000;

int a[MAXN][MAXN], dp[MAXN][MAXN];

int main() {
	int n, m;
	scanf("%d%d", &n, &m);
	for (int i = 0; i < n; ++i) {
		for (int j = 0; j < m; ++j) {
			scanf("%d", &a[i][j]);
		}
	}
	memset(dp, 0, sizeof(dp));
	int ans = 0;
	dp[0][0] = a[0][0];
	ans = max(ans, dp[0][0]);
	for (int i = 1; i < n; ++i) {
		dp[i][0] = a[i][0];
		ans = max(ans, dp[i][0]);
	}
	for (int i = 1; i < m; ++i) {
		dp[0][i] = a[0][i];
		ans = max(ans, dp[0][i]);
	}
	for (int i = 1; i < n; ++i) {
		for (int j = 1; j < m; ++j) {
			if (a[i][j] == 1) {
				dp[i][j] = min(dp[i - 1][j], min(dp[i][j - 1], dp[i - 1][j - 1])) + 1;
				ans = max(ans, dp[i][j]);
			}
		}
	}
	printf("%d\n", ans);
	return 0;
}
