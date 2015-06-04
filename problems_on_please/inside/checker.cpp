#include "testlib.h"

int main(int argc, char *argv[]) {
    setName("compares two signed integers");
    registerTestlibCmd(argc, argv);
    
    int correct = ans.readInt();
    int answer = ouf.readInt();
    
    if (correct != answer)
        quitf(_wa, "expected %d, found %d", correct, answer);
    
    quitf(_ok, "answer is %d", correct);
}