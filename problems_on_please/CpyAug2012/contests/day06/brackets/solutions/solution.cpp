#include<iostream>
#include <cstdio>

using namespace std;

void Gen(int n, int k, string Prefix)
{
	if(n==0)
		cout<<Prefix<<endl;
	else
	{
		if(k+1<=n-1)
			Gen(n-1,k+1,Prefix+"(");
		if(k>0)
			Gen(n-1,k-1,Prefix+")");
	}
}

int main()
{
    freopen("brackets.in", "r", stdin);
    freopen("brackets.out", "w", stdout);
    int n;
	cin>>n;
	Gen(2*n,0,"");
	return 0;
}
