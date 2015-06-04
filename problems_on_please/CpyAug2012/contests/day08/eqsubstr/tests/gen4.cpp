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
	for (int i = 0; i < len / 4; i++){
		root += z_rand('a', 'z');
	}

	str = root;
	for (int i = 0; i < 3; i++){
		root[z_rand(0, len / 4 - 1)] = z_rand('a', 'z');
		str += root;
	}

	cout << str << endl;
	cout << q << endl;
	for (int i = 0; i < q; i++){
		int p1 = z_rand(0, 3);
		int p2 = p1;
		while (p2 == p1){
			p2 = z_rand(0, 3);
		}
		int slen = z_rand(1, len / 4);
		int x1 = z_rand(1, len / 4 - slen + 1);
		int x2 = x1;
		cout << p1 * (len / 4) + x1 << " " << p1 * (len / 4) + x1 + slen - 1 << " ";
		cout << p2 * (len / 4) + x2 << " " << p2 * (len / 4) + x2 + slen - 1<< endl;
	}
	return 0;
}
