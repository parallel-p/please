#include "testlib.h"
#include <iostream>
using namespace std;

int main()
{
	registerValidation();
	int n = inf.readInt(0, 1000000);
	inf.readEoln();
	int last = 0, cur;
	for (int i = 0; i < n; i++)
	{
		cur = inf.readInt(0, 1000000000);
		ensure (last <= cur);
		last = cur;
		if (i + 1 < n)
			inf.readSpace();
	}
	inf.readEoln();
	int m = inf.readInt(1, 200000);
	inf.readEoln();
	for (int i = 0; i < m; i++)
	{
		inf.readInt(0, 1000000001);
		if (i + 1 < m) inf.readSpace();
	}
	inf.readEoln();
	inf.readEof();
	return 0;
}
