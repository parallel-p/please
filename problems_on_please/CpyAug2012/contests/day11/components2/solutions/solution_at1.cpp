#include <iostream>
#include <vector>
#include <set>
#include <cassert>
#include <cstdio>

#define sz(c) ((c).size())

using namespace std;

int vn = -1, en = -1;
vector<vector<int> > edl;
vector<int> col;
int dfs( int v, int c )
{
//  cerr << v << "\n";

  col[v] = c;
  for (int i = 0; i < sz(edl[v]); i++)
  {
    int to = edl[v][i];
    if (col[to] == -1)
      dfs(to, c);
  }
}

int main( int argc, char* argv[] )
{
  freopen("components2.in",  "rt", stdin);
  freopen("components2.out", "wt", stdout);

  int vn, en;
  cin >> vn >> en;

  edl.resize(vn);
  col.resize(vn, -1);

  cerr << en << "\n";

  for (int i = 0; i < en; i++)
  {
    int a, b;
    cin >> a >> b;
    a--, b--;
    edl[a].push_back(b);
    edl[b].push_back(a);
  }

  int curc = 0;
  for (int i = 0; i < vn; i++)
    if (col[i] == -1)
      dfs(i, curc++);

  vector<vector<int> > comps(curc);
  for (int i = 0; i < vn; i++)
    comps[col[i]].push_back(i);

  cout << curc << "\n";
  for (int i = 0 ; i < curc; i++)
  {
    cout << sz(comps[i]) << "\n";
    for (int j = 0; j < sz(comps[i]); j++)
      cout << comps[i][j] + 1 << " ";
    cout << "\n";
  }

  return 0;
}

