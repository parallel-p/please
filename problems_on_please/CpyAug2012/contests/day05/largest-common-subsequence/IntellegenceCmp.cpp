#include "testlib.h"
#include <stdio.h>

int main(int argc, char * argv[])
{
    setName("compare two signed int%d's", 8 * sizeof(int));
    registerTestlibCmd(argc, argv);
    
    int ja = ans.readInt();
    int pa = ouf.readInt();
    
    if (ja != pa)
        quitf(_wa, "expected %d, found %d", ja, pa);
    
	int a[1001];
	int i = 0;
	while(!inf.seekEoln()){
		a[i] = inf.readInt();
		i++;
	}
	
	int b[1001];
	int j = 0;
	while(!inf.seekEoln()){
		b[j] = inf.readInt();
		j++;
	}
	
	int n = i;
	int m = j;
	
	int cura = 0;
	int curb = 0;
	for(i = 0; i < ja; i++){
		int tmp = ouf.readInt();
		bool isInA = false;
		for(; cura < n; cura++){
			if(a[cura] == tmp){
				isInA = true;
				break;
			}
		}
		bool isInB = false;
		for(; curb < m; curb++){
			if(b[curb] == tmp){
				isInB = true;
				break;
			}
		}
		if(!(isInA and isInB)){
			quitf(_wa, "wrong sequence");
		}
	}
	
    quitf(_ok, "answer is %d", ja);
}
