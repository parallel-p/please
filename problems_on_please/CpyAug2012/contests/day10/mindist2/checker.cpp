#include "testlib.h"
#include <set>

using namespace std;

set<pair<int, int> > S;

int main(int argc, char * argv[]) {
    registerTestlibCmd(argc, argv);
    int n = inf.readInt(), m = inf.readInt();
    int a = inf.readInt(), b = inf.readInt();
    int rans = ans.readInt();
    int gans = ouf.readInt();
    if (gans != rans)
        quitf(_wa, "Answer is %d but contestant says that it is %d.", rans, gans);
    if (gans == -1)
        quitf(_ok, "ok there is no path");
    for (int i = 0; i < m; i++)
    {
        int p, q;
        p = inf.readInt();
        q = inf.readInt();
        S.insert(make_pair(p, q));
        S.insert(make_pair(q, p));
    }
    int u = -1, v = ouf.readInt();;
    for (int i = 0; i < rans; i++)
    {
        u = v;
        v = ouf.readInt();
        if (S.find(make_pair(u, v)) == S.end())
            quitf(_wa, "There is no edge (%d, %d).", u, v);
    }
    quitf(_ok, "ok");
}
