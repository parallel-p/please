#include <stdio.h>

const int MAXN = 5010;
const int MAXM = 2 * 100100 + MAXN;

int s = 0;
int t = 0;
int N = 0;
int M = 0;
int count = MAXN + 1;
int items[MAXM] = {0};
int next[MAXM] = {0};
int w[MAXM] = {0};
int d[MAXN] = {0};
int color[MAXN] = {0};

void init() {
	for (int i = 0; i < MAXM; ++i) {next[i] = -1;}
	for (int i = 0; i < MAXN; ++i) {d[i] = -1;}
}

void add(int u, int v, int ww) {
	items[count] = v;
	w[count] = ww;
	next[count] = next[u];
	next[u] = count;
	count++;
}

void read() {
	scanf("%d %d %d %d", &N, &M, &s, &t);
	for (int i = 0; i < M; ++i) {
		int u = 0; int v = 0; int w = 0;
		scanf("%d %d %d", &u, &v, &w);
		add(u, v, w);
		add(v, u, w);
	}
}

void relax(int u, int v, int w) {
	if ((-1 == d[v]) || (d[v] > d[u] + w)) {
		d[v] = d[u] + w;
	}
}

void dijkstra(int s) {
	d[s] = 0;
	for (int k = 0; k < N; ++k) {
		int u = -1;
		for (int i = 1; i <= N; ++i) {
			if ((0 == color[i]) && (-1 != d[i]) && (-1 == u || d[u] > d[i])) {
				u = i;
			}
		}
		int iter = next[u];
		while (-1 != iter) {
			relax(u, items[iter], w[iter]);
			iter = next[iter];
		}
		color[u] = 1;
	}
}

int main(void) {
	freopen("distance.in", "rt", stdin);
	freopen("distance.out", "wt", stdout);
	init();
	read();
	dijkstra(s);
	printf("%d", d[t]);
	return 0;
}
