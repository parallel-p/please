#include "testlib.h"
#include <vector>
#include <set>
#include <utility>
#include <iostream>
#include <string>
using namespace std;
int main(int argc, char * argv[]) {
    registerTestlibCmd(argc, argv);
    char contestant_ans = ouf.readChar();
    char correct_ans = ans.readChar();
    if (correct_ans != contestant_ans)
        quit(_wa, "answers don't match");
    quit(_ok, "");
}