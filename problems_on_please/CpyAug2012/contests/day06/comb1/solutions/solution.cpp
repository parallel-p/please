#include<iostream>
#include <cstdio>

using namespace std;

void Gen(int n, int k, string Prefix)
{
	if(n==0)
		cout<<Prefix<<endl;
	else
	{
		if(n>k)
			Gen(n-1, k,Prefix+"0 ");
		if(k>0)
			Gen(n-1, k-1,Prefix+"1 ");
	}
}

int main()
{
    freopen("comb1.in", "r", stdin);
    freopen("comb1.out", "w", stdout);
	int n, k;
	cin>>n>>k;
	Gen(n,k,"");
	return 0;
}
