#include <iostream>
#include <vector>
#include <set>
#include <cassert>

#include "testlib.h"

#define sz(c) ((c).size())

using namespace std;

int vn = -1, en = -1;
vector<vector<int> > edl;
vector<int> col;
vector<vector<int> > comps;
int dfs( int v, int c )
{
  col[v] = c;
  comps[c].push_back(v + 1);
  for (int i = 0; i < sz(edl[v]); i++)
  {
    int to = edl[v][i];
    if (col[to] == -1)
      dfs(to, c);
  }
}

int main( int argc, char* argv[] )
{
  setName("check graph components");
  registerTestlibCmd(argc, argv);

  vn = inf.readInt();
  en = inf.readInt();
  edl.resize(vn);
  col.resize(vn, -1);

  for (int i = 0; i < en; i++)
  {
    int a = inf.readInt();
    int b = inf.readInt();
    a--, b--;
    edl[a].push_back(b);
    edl[b].push_back(a);
  }

  int curc = 0;
  for (int i = 0; i < vn; i++)
    if (col[i] == -1)
    {
      comps.push_back(vector<int>());
      dfs(i, curc++);
      sort(comps.back().begin(), comps.back().end());
    }

  assert(curc == sz(comps));

  int outCompCount = ouf.readInt();
  if (outCompCount != curc)
    quitf(_wa, "expected %d components, found %d", curc, outCompCount);

  set<vector<int> > outComps;
  for (int c = 0; c < curc; c++)
  {
    int outVN = ouf.readInt();
    if (!(1 <= outVN && outVN <= vn))
      quitf(_wa, "incorrect vertices number in component: %d", outVN);

    vector<int> outComp(outVN);
    for (int i = 0; i < outVN; i++)
      outComp[i] = ouf.readInt();
    sort(outComp.begin(), outComp.end());
    outComps.insert(outComp);
  }
  
  if (set<vector<int> >(comps.begin(), comps.end()) != outComps)
    quitf(_wa, "answers dont match");

  quitf(_ok, "components number is %d", curc);

  return 0;
}

