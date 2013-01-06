#include "testlib.h"

using namespace std;

int main() {
    registerValidation();
	int n = inf.readInt(1, 100000, "N");
	inf.readSpace();
	int m = inf.readInt(1, 100000, "M");
	inf.readEoln();
	for (int i = 0; i < m; ++i) {
		inf.readInt(1, n, "from[" + vtos(i + 1) + "]");
		inf.readSpace();
		inf.readInt(1, n, "to[" + vtos(i + 1) + "]");
		inf.readEoln();
	}
	inf.readEof();
    return 0;
}
