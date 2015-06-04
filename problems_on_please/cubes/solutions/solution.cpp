#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

int n, m;
vector <int> masha(100000), pasha(100000);
int ansmasha[100000], anspasha[100000], intersect[100000];
int ansmi=0, anspj=0, ansintk=0;
int main()
{
    cin >> n >> m;
    for(int i = 0; i < n; i++)
        cin >> masha[i];
    for(int i = 0; i < m; i++)
        cin >> pasha[i];
    sort(masha.begin(), masha.begin()+n);
    sort(pasha.begin(), pasha.begin()+m);
    int i = 0, j = 0;
    while(i < n && j < m)
    {
        if(masha[i] < pasha[j])
            ansmasha[ansmi++]=masha[i++];
        else if(masha[i] > pasha[j])
            anspasha[anspj++]=pasha[j++];
        else if(masha[i] == pasha[j])
        {
            intersect[ansintk++]=masha[i];
            i++; j++;
        }
    }
    for(; i < n; i++, ansmi++)
        ansmasha[ansmi]=masha[i];
    for(; j < m; j++, anspj++)
        anspasha[anspj]=pasha[j];
    cout << ansintk << " ";
    for(int a = 0; a < ansintk; a++)
        cout << intersect[a] << " ";
    cout << endl;
    cout << ansmi << " ";
    for(int a = 0; a < ansmi; a++)
        cout << ansmasha[a] << " ";
    cout << endl;
    cout << anspj << " ";
    for(int a = 0; a < anspj; a++)
        cout << anspasha[a] << " ";
    return 0;
}
