#include <stdio.h>

#define MAXN (15)

int color[MAXN] = {0};
int N = 0;
int M = 0;

int fact(int n) {
	int res = 1;
	for (int i = 2; i <= n; i++)
		res *= i;
	return res;
}

int main() {
	freopen("bynumber.in", "rt", stdin);
	freopen("bynumber.out", "wt", stdout);

	scanf("%d %d", &N, &M);
	for (int i = N - 1; i >=0; i--) {
		int iFact = fact(i);
		int ind = M / iFact;
		M %= iFact;
		int pos = 0;
		for (int j = 0; j < N; j++) {
			if (color[j]) continue;
			if (pos == ind) {
				printf("%d ", j + 1);
				color[j] = 1;
				break;
			}
			pos++;
		}
	}

	return 0;
}
