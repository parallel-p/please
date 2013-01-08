#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <iostream>
#include <vector>
#include <utility>
#include <algorithm>
#include <iterator>
#include <set>
#include <map>
#include <sstream>

#include "testlib.h"

using namespace std;

int main()
{
    registerValidation();

	int n = inf.readInt(1, 100000);
	inf.readSpace();
	int m = inf.readInt(0, 100000);
	inf.readEoln();

    set<pair<int, int> > edges;
    vector<pair<int, int> > edges_r;
    for (int i = 0; i < m; ++i) {
        int x, y;
        x = inf.readInt(1, n);
		inf.readSpace();
		y = inf.readInt(1, n);
		inf.readEoln();
        ensure(edges.insert(make_pair(x, y)).second);
    }
    inf.readEof();

    return 0;
}
