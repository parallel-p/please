#include <cstdio>

const int MAXN = 50;

int N = 0;
int seq[MAXN] = {0};

void print(int len) {
	for (int i = 0; i < len; i++) {
		printf("%d ", seq[i]);
	}
	puts("");
}

void generate(int sum, int len, int min) {
	if (N == sum) {
		print(len);
	}
	int M = (min < (N - sum)) ? min : N - sum;
	for (int i = 1; i <= M; i++) {
		seq[len] = i;
		generate(sum + i, len + 1, (i < min) ? i : min);
	}
}

int main(void) {
	freopen("partition.in", "rt", stdin);
	freopen("partition.out", "wt", stdout);
	scanf("%d", &N);
	generate(0, 0, N);
	return 0;
}
