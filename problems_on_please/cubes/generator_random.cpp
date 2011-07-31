#include <iostream>
#include <cstdlib>
#include <ctime>

using namespace std;

int main(int argc, char* argv[])
{
    srand(atoi(argv[1]));
    int n, m, t;
    n = rand() % (100 * 1000 + 1);
    m = rand() % (100 * 1000 + 1);
    cout << n << " " << m << endl;
    for(int i = 1; i <= n; i++)
    {
        t = rand() % (1000 * 1000 * 1000 + 1);
        cout << t << endl;
    }
    for(int i = 1; i <= m; i++)
    {
        t = rand() % (1000 * 1000 * 1000 + 1);
        cout << t << endl;
    }
    cout << endl;
    return 0;
}

