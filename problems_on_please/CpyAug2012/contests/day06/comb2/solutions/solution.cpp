#include<iostream>
#include<cstdio>

using namespace std;

char buff[11];

void Gen(int n, int k, int last, string Prefix)
{
	if(n==0)
		cout<<Prefix<<endl;
	else
	{
		for(int i=last+1;i+n-1<=k;++i)
		{
			sprintf(buff,"%d ",i);
			Gen(n-1,k,i,Prefix+buff);
		}
	}
}

int main()
{
    freopen("comb2.in", "r", stdin);
    freopen("comb2.out", "w", stdout);
	int n, k;
	cin>>n>>k;
	Gen(n, k, 0, "");
	return 0;
}
