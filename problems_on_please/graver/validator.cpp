#include "testlib.h"

using namespace std;

int main() {
    registerValidation();
    for (int i = 0; i < 26; i++) {
        inf.readInt(1, 1000);
        inf.readLine();
    }
    inf.readWord("[a-z]{1,1000}");
    return 0;
}
