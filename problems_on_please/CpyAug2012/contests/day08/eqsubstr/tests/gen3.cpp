#include "rand.h"
#include <cassert>
#include <iostream>
#include <string>
#include <cstdlib>

using namespace std;

string str, root;
int len, q;

int main(int argc, char * argv[]){
    assert(argc >= 3);
    int len = atoi(argv[1]);
    int q = atoi(argv[2]);
    int rndsd = atoi(argv[3]);
    srand(rndsd);
	for (int i = 0; i < len / 3; i++){
		root += z_rand('a', 'z');
	}
	str = root;
	int pos = z_rand(0, len / 3 - 1);
	char oldc = root[pos];
	root[pos] = z_rand('a', 'z');
	
	str += root;
	root[pos] = oldc;
	str += root;

	cout << str << endl;
	cout << q << endl;
	for (int i = 0; i < q; i++){
		int p1 = z_rand(0, 2);
		int p2 = z_rand(0, 2);
		int slen = z_rand(1, len / 3);
		int x1 = z_rand(1, len / 3 - slen + 1);
		int x2 = x1;
		cout << p1 * (len / 3) + x1 << " " << p1 * (len / 3) + x1 + slen - 1 << " ";
		cout << p2 * (len / 3) + x2 << " " << p2 * (len / 3) + x2 + slen - 1<< endl;
	}
	return 0;
}
