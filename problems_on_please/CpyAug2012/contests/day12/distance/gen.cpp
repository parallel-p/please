#include "testlib.h"
#include <iostream>

using namespace std;

int main(int argc, char* argv[])
{
    registerGen(argc, argv);
    int n = atoi(argv[1]);
    int m = atoi(argv[2]);
    int a[m + 1], b[m + 1];
    int p[n + 1];
    int c = 0;
    int last = (n * (n - 1)) / 2;
    int num = last / m;


  for (int i = 1; i <= n - 1; ++i) {
    for (int j = i + 1; j <= n; ++j) {
      if (c < m) {
        if ((rnd.next(0, num) == 0) || (last == m - c)) {
          ++c;
          a[c] = i;
          b[c] = j;
        }
      }
      --last;
    }
  }

  p[1] = 1;
  for (int i = 2; i <= n; ++i) {
      int j = rnd.next(1, i);
      p[i] = p[j];
      p[j] = i;
  }

  cout << n << " "  << c << endl;
  int s = rnd.next(1, n);
  int t = s;
  while (t == s) {
    t = rnd.next(1, n);
  }
  cout << s << " " << t << endl;
  for (int i = 1; i <= c; ++i) {
    cout << p[a[i]] << " " << p[b[i]] << " " << rnd.next(1, 100000) << endl;
  }
    return 0;
}
