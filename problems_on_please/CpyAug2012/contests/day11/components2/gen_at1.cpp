#include <iostream>
#include <vector>
#include <set>
#include <cassert>

#include "random.h"

#define sz(c) ((c).size())
#define mp make_pair

using namespace std;
typedef pair<int, int> pii_t;

int main( int argc, char* argv[] )
{
  initrand(30);
  if (argc >= 2)
    initrand(atoi(argv[1]));

  int vn = 100000;
  if (argc >= 3)
    vn = atoi(argv[2]);

  int en = 100000;
  if (argc >= 4)
    en = atoi(argv[3]);

  set<pii_t> edges;

  for (int i = 0; i < en; i++)
  {
    while (true)
    {
      int a = rndInt(vn);
      int b = rndInt(vn);

//      cout << a << " " << b << "\n";
      if (a != b && !edges.count(mp(a, b)) && !edges.count(mp(b, a)))
      {
        edges.insert(mp(a, b));
        break;
      }
    }
  }

  vector<pii_t> ve(edges.begin(), edges.end());
  for (int i = 0; i < 2 * sz(ve); i++)
    swap(ve[rndInt(sz(ve))], ve[rndInt(sz(ve))]);

  cout << vn << " " << en << "\n";
  for (vector<pii_t>::iterator i = ve.begin(); i != ve.end(); ++i)
    cout << i->first + 1 << " " << i->second + 1 << "\n";

  return 0;
}
