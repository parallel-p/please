#include <cstdlib>
#include <cstdio>
#include <algorithm>

const int n = 100000;
int q[n];
int qq[n];

int main()
{
	srand(14814127);
	printf("%d %d\n", n, n-1);
	for (int i=0; i<n; ++i)
	{
		qq[i] = i;
		q[i] = i+1;
	}
	std::random_shuffle(q, q+n);
	std::random_shuffle(qq, qq+n-1);
	for (int i=0; i<n-1; ++i)
		printf("%d %d\n", q[qq[i]], q[qq[i]+1]);
	return 0;
}
