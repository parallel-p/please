#include <cstdlib>
#include <cstdio>
#include <algorithm>

int n = 100000;
int m = 100000;

int main()
{
	srand(5017524);
	printf("%d %d\n", n, m);
	int q[n];
	for (int i=0; i<n; ++i)
		q[i] = i+1;
	std::random_shuffle(q, q+n);
	--n;
	for (int i=0; i<m; ++i)
		printf("%d %d\n", q[n], q[rand() % n]);
	return 0;
}
