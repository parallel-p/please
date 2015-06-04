#include <iostream>
#include <string>

using namespace std;

int main (int argc, char * const argv[]) {
    int cost[26];

    for (int i = 0; i < 26; i++) {
        cin >> cost[i];
    }

    string s;
    cin >> s;
    cin >> s;
    int sum = 0;
    for (int i = 0; i < s.length(); i++) {
        sum += cost[s[i] - 'a'];
    }
    cout << sum;
    
    return 0;
}
