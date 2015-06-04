#include <iostream>
#include <map>
#include <iostream>
#include <string>

using namespace std;

int main () 
{
    int numbers = 0;
    cin >> numbers;
    string key = "";
    string value = "";
    map <string, string> dict;
    for (int i = 0; i < numbers; i++)
    {
       cin >> key;
       cin >> value;
       dict [key] = value;
       dict [value] = key;
    }
    string to_translate = "";
    cin >> to_translate;
    cout << dict [to_translate];
    //cin >> key;  
    return 0;
}
