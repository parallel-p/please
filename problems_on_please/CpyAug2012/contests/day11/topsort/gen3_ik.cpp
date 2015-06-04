#include <cstdlib>
#include <cstdio>
#include <algorithm>

int n = 100000;

int main()
{
	srand(5358390);
	printf("%d %d\n", n, n-1);
	int q[n];
	for (int i=0; i<n; ++i)
		q[i] = i+1;
	std::random_shuffle(q, q+n);
	for (int i=1; i<n; ++i)
		if (rand() % 2)
			printf("%d %d\n", q[0], q[i]);
		else
			printf("%d %d\n", q[i], q[0]);
	return 0;
}
