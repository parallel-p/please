#include "rand.h"
#include <iostream>
#include <cassert>
#include <string>
#include <cstdlib>

using namespace std;

string str;
int len, q;

int main(int argc, char * argv[]){
    assert(argc >= 3);
    int len = atoi(argv[1]);
    int rndsd = atoi(argv[2]);
	srand(rndsd);
	for (int i = 0; i < len; i++){
		str += "p";
	}
	cout << str << endl;
	q = 100000;
	cout << q << endl;
	for (int i = 0; i < q; i++){
		int slen = z_rand(1, len);
		int l1 = z_rand(1, len-slen+1);
		int l2 = z_rand(1, len-slen+1);
		cout << l1 << " " << l1 + slen - 1 << " " << l2 << " " << l2 + slen - 1 << endl;
	}
	return 0;

}
