#include <cstdio>
#include <map>

using namespace std;

int main() {
  map <int, int> r;
  int n, m;
  for (int i = 0; i < n; i++) {
    int a;
    scanf("%d", &a);
    r[a] = r[a] + 1;
  }
  for (int i = 0; i < m; i++) {
    int a;
    scanf("%d", &a);
    printf("%d\n", r[a]);
  }
  return 0;
}
