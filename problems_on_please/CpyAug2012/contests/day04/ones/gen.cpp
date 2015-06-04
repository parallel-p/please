#include "testlib.h"
#include <iostream>
#include <algorithm>
#include <functional>
#include <vector>	

using namespace std;

int main(int argc, char** argv) {
    registerGen(argc, argv);

    int n = atoi(argv[1]); 
    cout << n << endl;
    return 0;
}