#include<iostream>
#include <cstdio>
using namespace std;

void Gen(int n, int k, string Prefix)
{
	if(n==0)
		cout<<Prefix<<endl;
	else
	{
		for(char c='0';c<'0'+k;++c)
		Gen(n-1,k,Prefix+string(1,c)+" ");
	}
}

int main()
{
    freopen("numbers.in", "r", stdin);
    freopen("numbers.out", "w", stdout);
	int n, k;
	cin>>n>>k;
	Gen(n,k,"");
	return 0;
}
