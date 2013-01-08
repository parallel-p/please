#include "testlib.h"
#include<set>
#include<vector>

using namespace std;

vector<set<int> > G;
int N, M;

int main(int argc, char * argv[]) {
    string YesNoAnswer1, YesNoAnswer2;
    int i, a, b;
    int CycleLength;
    vector <int> Cycle;
    registerTestlibCmd(argc, argv);
    N = inf.readInt(1, 100000, "N");
    M = inf.readInt(0, 100000, "M");
    G.resize(N + 1);
    for (i = 0; i < M; ++i)
    {
        a = inf.readInt(1, N, "Edge start");
        b = inf.readInt(1, N, "Edge end");
        G[a].insert(b);
    }
    YesNoAnswer1 = ans.readString();
    YesNoAnswer2 = ouf.readString();
    if (YesNoAnswer1 != "YES" && YesNoAnswer1 != "NO")
        quit(_fail, "First line of answer must be YES or NO\n");
    if (YesNoAnswer2 != "YES" && YesNoAnswer2 != "NO")
        quit(_pe, "First line of output must be YES or NO\n");
    if (YesNoAnswer1 != YesNoAnswer2)
        quit(_wa, "First line of answer is incorrect\n");
    if (YesNoAnswer1 == "NO")
        quit(_ok, "OK, NO\n");
    CycleLength = ouf.readInt(1, N, "Cycle length");
    for (i = 0; i < CycleLength; ++i)
    {
        Cycle.push_back(ouf.readInt(1, N, "Cycle vertex"));
    }
    Cycle.push_back(Cycle[0]);
    for (i = 1; i < Cycle.size(); ++i)
    {
        if (G[Cycle[i - 1]].count(Cycle[i]) == 0)
        {
            quitf(_wa, "Wrong edge in cycle: %d %d\n", Cycle[i - 1], Cycle[i]);
        }
    }
    quit(_ok, "OK, YES\n");
}
