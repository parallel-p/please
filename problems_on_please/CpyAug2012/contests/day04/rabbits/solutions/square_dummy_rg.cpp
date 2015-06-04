#include <iostream>
#include <stdio.h>
#include <math.h>

using namespace std;

const int MAXN = 1000;
int n, m;
int a[MAXN][MAXN];

bool check(int x, int y, int bound) {
	for (int i = x; i < x + bound; ++i) {
		for (int j = y; j < y + bound; ++j) {
			if (a[i][j] == 0) {
				return false;
			}
		}
	}
   return true;
}

int main() {
	

	cin >> n >> m;
	
	int maxLength = 0;
	for (int i = 0; i < n; ++i) {
		for (int j = 0; j < m; ++j) {
			cin >> a[i][j];
		}
	}

	for (int i = 0; i < n; ++i) {
		for (int j = 0; j < m; ++j) {
			for (int k = 1; k < n - i + 1 && k < m - j + 1; ++k) {
				if (check(i, j, k)) {
					//cout << k << endl;
					maxLength = max(maxLength, k);
				}
			}					
		}
	}
	cout << maxLength;
	return 0;	
}
