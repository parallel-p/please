#include<iostream>
#include<vector>
#include<cstdio>

using namespace std;

vector<int> mask;

char buff[11];

void Gen(int n, string Prefix)
{
	bool print=1;
	for(int i=1;i<=n;++i)
	{
		if(mask[i])
		{
			mask[i]=0;
			sprintf(buff,"%d ",i);
			Gen(n,Prefix+buff);
			print=0;
			mask[i]=1;
		}
	}
	if(print)
		cout<<Prefix<<endl;
}

int main()
{
    freopen("permutations.in", "r", stdin);
    freopen("permutations.out", "w", stdout);
	int n;
	cin>>n;
	mask.resize(n+1,1);
	Gen(n, "");
	return 0;
}
