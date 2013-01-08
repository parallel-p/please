#include <stdio.h>
#include <iostream>
#include <string>
#include <stdlib.h>
#include <ctime>
#include <vector>
#include <utility>
#include <algorithm>

using namespace std;

vector<int> ropes;
long long n, k;

long long count(int len)
{
    long long num = 0;
    for(int i = 0; i < n; i++)
    {
        num += ropes[i]/len;
    }
    return num;
}

int main()
{
    freopen("ropes.in", "r", stdin);
    freopen("ropes.out", "w", stdout);
    cin >> n >> k;
    for(int i = 0; i < n; i++)
    {
        int temp;
        cin >> temp;
        ropes.push_back(temp);
    }
    int l = 0;
    int r = 100000001;
    while(r - l > 1)
    {
        int m = (l + r) / 2;
        if(count(m) < k)
            r = m;
        else
            l = m;
    }
    cout << l;
    return 0;
}