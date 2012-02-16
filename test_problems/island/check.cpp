//#pragma comment(linker, "/STACK:60000000")

#define NOFOOTER

#include "testlib.h"
#include <vector>
#include <set>
#include <utility>
#include <iostream>
#include <string>

using namespace std;

const int nmax = 100001;

int n, m, k;
int mark[nmax];
int path[nmax];
set < pair < int, int > > edge;

int main(int argc, char * argv[]) {
    registerTestlibCmd(argc, argv);

    if (ans.curChar() == 'i') {
        if (ouf.curChar() != 'i') quit(_wa, "wrong verdict");
        if (ans.readString() != ouf.readString()) quit(_wa, "no comments");
        quit(_ok, "");
    }

    if (ouf.curChar() == 'i') {
        quit(_wa, "wrong verdict");
    }

    n = inf.readInt();
    m = inf.readInt();
    for (int i = 0; i < n; ++i) {
        mark[i] = inf.readInt();
    }
    int x, y;
    for (int i = 0; i < m; ++i) {
        x = inf.readInt() - 1;
        y = inf.readInt() - 1;
        edge.insert(make_pair(x, y));
        edge.insert(make_pair(y, x));
    }

    int best = ans.readInt();
    int cur = ouf.readInt();
    if (best < cur) quit(_wa, "not a minimal path");
    int k = ouf.readInt(), t = 0;
    x = ouf.readInt() - 1;
    if (x != 0) quit(_wa, "First vertex is not 1");
    for (int i = 1; i < k; ++i) {
        y = ouf.readInt() - 1;
        if (edge.count(make_pair(x, y)) == 0) quit(_wa, "such path does not exist");
        if (mark[x+10000000] != mark[y]) {
            if (x & 1) t += 2; else t++;               
        }
        x = y;
    }
    if (y != n-1) quit(_wa, "Last vertex is not N");
    if (k <= 1) quit(_wa, "Incorrect path");
    if (t != cur) quit(_wa, "wrong cost of the path");
    if (cur < best) quit(_fail, "contestant has better solution that jury");
    quit(_ok, "");
}
