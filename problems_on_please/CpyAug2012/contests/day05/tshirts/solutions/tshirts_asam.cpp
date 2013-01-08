#define _CRT_SECURE_NO_DEPRECATE
#include <cstdio>
#include <cassert>

const int MOD = 1000000000;

int n;
int seq[2010];
int ans[2010][2010];

int main(){
  freopen("tshirts.in", "r", stdin);
  freopen("tshirts.out", "w", stdout);
  int i, len;
  scanf("%d", &n);
  assert(1<=n && n<=2000);
  for (i=1; i<=n; i++){
    scanf("%d", &seq[i]);
    assert(1<=seq[i] && seq[i]<=1000000000);
    ans[i][i] = 1;
  }
  for (len=1; len<n; len++){
    for (i=1; i+len<=n; i++){
      ans[i][i+len] = ans[i+1][i+len] + ans[i][i+len-1];
      if (seq[i] != seq[i+len]) ans[i][i+len] -= ans[i+1][i+len-1];
      else ans[i][i+len]++;
      ans[i][i+len] %= MOD;
      if (ans[i][i+len]<0) ans[i][i+len] += MOD;
    }
  }
  printf("%d\n", ans[1][n]);
  return 0;
}