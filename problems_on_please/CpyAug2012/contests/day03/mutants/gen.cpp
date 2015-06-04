#include "random.h"

#include <cassert>
#include <cstdio>
#include <cstdlib>
#include <algorithm>

using namespace std;

const int maxN = 1000000;

int q[maxN];
int n, m, rn, rm;

int main( int argc, char *argv[] ) {
  assert(argc == 6);
  n = atoi(argv[1]);
  m = atoi(argv[2]);
  initrand(atoi(argv[3]));
  rn = atoi(argv[4]);
  rm = atoi(argv[5]);
  for (int i = 0; i < n; i++) {
    q[i] = R(0, rn);
  }
  sort(q, q + n);
  for (int i = 0; i < n; i++) {
  	if (i != 0)
  		printf(" ");
    printf("%d", q[i]);
  }
  printf("\n");

  for (int i = 0; i < m; i++) {
  	if (i != 0)
  		printf(" ");
    printf("%d", R(0, rm));
  }
  printf("\n");
  return 0;
}
