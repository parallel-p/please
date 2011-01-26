
#include <cstdio>
#include <cstdlib>

int main() {
  static const int n = 921;
  int d[n][n];
  for (int i = 0; i < n; i++)
    for (int j = 0; j < n; j++)
      d[i][j] = rand();
  for (int k = 0; k < n; k++)
    for (int i = 0; i < n; i++)
      for (int j = 0; j < n; j++)
        if (d[i][j] > d[i][k] + d[k][j])
          d[i][j] = d[i][k] + d[k][j];
  return 0;
}

