#include <string>
#include <set>
#include <iostream>
#include <fstream>

using namespace std;

int main(){
    ifstream in;
    ofstream out;
    in.open("spell.in");
    out.open("spell.out");
    set<string> words;
    string s;
    int t = 0;
    while(in>>s){
        words.insert(s);
    }

    out<<words.size();

    in.close();
    out.close();
}
