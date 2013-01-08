#include "testlib.h"

using namespace std;

int main() 
{
    registerValidation();

    int n = inf.readInt(1, 5000);

    inf.readEoln();

    for (int i = 0; i < n; ++i) {
        inf.readInt(1, 3600);
        inf.readSpace();
        inf.readInt(1, 3600);
        inf.readSpace();
        inf.readInt(1, 3600);
        inf.readEoln();        
    }

    inf.readEof();
    return 0;
}
