#include <cstdio>
#include <cstdlib>
#include <algorithm>
#include "testlib.h"

using namespace std;

void rand_shuffle(int *b, int k)
{
    for (int i=0; i<k; i++)
    {
        int x = rnd.next(0,i);
        int e = b[i];
        b[i] = b[x];
        b[x] = e;
    }
}


int a[100010],b[100010];

int main(int argc, char* argv[]){
  
	int n = atoi(argv[1]);
	int k = atoi(argv[2]);
    int Max = atoi(argv[3]);
	int seed = atoi(argv[4]);

    registerGen(argc, argv);


    for (int i=0; i<n; i++)
    {
        a[i] = rnd.next(1, Max);    
    }

    sort(a,a+n);

    int y = rnd.next(0,k);

    for (int i=0; i<y; i++)
    {
        b[i] = a[rnd.next(0,n-1)];
    }

    for (int i=y; i<k; i++)
    {
        b[i]=rnd.next(1,Max);
        while (binary_search(a, a+n, b[i])) b[i]=rnd.next(1,Max);
    }

    rand_shuffle(b,k);

    for (int i=0; i<n; i++)
    {
        printf("%d",a[i]);
        if (i<n-1) printf(" "); else printf("\n");
    }
    for (int i=0; i<k; i++)
    {
        printf("%d",b[i]);
        if (i<k-1) printf(" "); else printf("\n");
    }    
  
	return 0;
}
