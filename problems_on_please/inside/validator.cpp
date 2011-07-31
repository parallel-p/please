#include "testlib.h"
#include <iostream>

using namespace std;

int main() {
    registerValidation();
    for (int t = 0; t < 2; t++) {
        int n = inf.readInt(0, (int)1e4);
        inf.readEoln();
        for (int i = 0; i < n; i++) {
            string s = inf.readToken();
            int len = s.length();
            if (len > 300)
                quitf(_fail, "length of some number is more than 300");             
            if (i < n - 1) {
                char ch = inf.readChar();
                if (ch != ' ')
                    quitf(_fail, "unexpected char {%c}, expected whitespace", ch);             
            }
        }
        inf.readEoln();
    }
    inf.readEof();
    return 0;
}
