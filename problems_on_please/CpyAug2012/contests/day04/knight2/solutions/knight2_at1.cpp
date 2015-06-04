#define _CRT_SECURE_NO_WARNINGS
#include <cstdio>
#include <cstring>
#include <cassert>
#include <cstdlib>
#include <ctime>
#include <cmath>

#include <algorithm>
#include <sstream>
#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <set>

#define sz(c) ((int)(c).size())
#define pb push_back
#define mp make_pair

#define REP(i, n) for (int i = 0; i < (n); ++i)
#define REPC(i, c) for (typeof((c).begin()) i = (c).begin(); i != (c).end(); ++i)
#define FOR(i, s, n) for (int i = (s); i < (n); ++i)
#define ALL(c) (c).begin(), (c).end()

using namespace std;
typedef long long ll;
typedef double dbl;
typedef pair<int, int> pii;


struct Big
{
  static const int LEN = 50;
  int num[LEN];

  Big( int a = 0 )
  {
    memset(num, 0, sizeof(num));
    for (int i = 0; a; a /= 10)
      num[i] = a % 10;
  }

  void normalize()
  {
    REP(i, LEN - 1)
      if (num[i] >= 10)
        num[i] -= 10, ++num[i + 1];
  }

  Big& operator += ( Big const& u )
  {
    REP(i, LEN)
      num[i] += u.num[i];
    normalize();
    return *this;
  }
};

ostream& operator << ( ostream& istr, Big const& u )
{
  int p = Big::LEN - 1;
  for (; p > 0 && !u.num[p]; --p)
    ;
  for (; p >= 0; --p)
    istr << u.num[p];
  return istr;
}

// typedef long long Big;

int main()
{
  int h, w;
  cin >> w >> h;

  vector<vector<Big> > dp(h + 3, vector<Big>(w + 3));
  dp[2][2] = 1;
  int dx[] = {-2, -2, +1, -1};
  int dy[] = {+1, -1, -2, -2};
  REP(i, h)
    for (int y = i + 2, x = 2; x < w + 2 && y >= 2; x++, y--)
      REP(d, 4)
        dp[y][x] += dp[y + dy[d]][x + dx[d]];
  REP(i, w - 1)
    for (int y = h + 1, x = i + 3; x < w + 2 && y >= 2; x++, y--)
      REP(d, 4)
        dp[y][x] += dp[y + dy[d]][x + dx[d]];
//  REP(y, h) {
//    REP(x, w)
//      cout << dp[y + 2][x + 2] << " ";
//    cout << endl;
//  }
  cout << dp[h + 1][w + 1] << endl;

  return 0;
}
