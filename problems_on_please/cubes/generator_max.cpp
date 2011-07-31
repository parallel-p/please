#include <iostream>
#include <cstdlib>
#include <ctime>

using namespace std;

int main(int argc, char* argv[])
{
    srand(atoi(argv[1]));
    int n, m, t;
    n = 100000;
    m = 100000;
    cout << n << " " << m << endl;
    int v[100000];
    for(int i = 1; i <= n; i++)
    {
        t = rand() % (1000 * 1000 * 1000 + 1);
        cout << t << endl;
        v[i-1]=t;
    }
    for(int i = 1; i <= m; i++)
    {
        cout << v[i-1] << endl;
    }
    cout << endl;
    return 0;
}

