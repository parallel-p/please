#include <iostream>
#include <ctime>
#include <cstdlib>
#include <vector>
#include <cstdio>
#include <algorithm>
using namespace std;

#define TASK "pants"
int main (int argc, char * const argv[]) 
{
    freopen(TASK ".in", "r", stdin);
    freopen(TASK ".out", "w", stdout);
    int n;
    cin >> n;
    int t;
    vector<int> v;
    for (int i = 0; i < n; i++)
        cin >> t, v.push_back(t);
    sort(v.begin(), v.end());
    cout << unique(v.begin(), v.end()) - v.begin();
    srand(time(NULL));
 
    return 0;
}
