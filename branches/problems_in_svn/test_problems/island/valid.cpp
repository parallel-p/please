#include "testlib.h"

int main() {
    registerValidation();
	int n = inf.readInt(1, 100000);
	inf.readSpace();
	int m = inf.readInt(1, 100000);
	inf.readEoln();
	for (int i = 0; i < n; i++) {
		if (i) inf.readSpace();
		inf.readInt(1, 2);
	}
	inf.readEoln();
	for (int i = 0; i < m; i++) {
		int u = inf.readInt(1, n);
		inf.readSpace();
		ensuref(u != inf.readInt(1, n), "There is a loop in the graph");
		inf.readEoln();
	}
	inf.readEof();
	return 0;
}
