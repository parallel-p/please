#include<iostream>
#include <cstdio>

using namespace std;

int m,n,rez[31],ans[31],a[16],b[16];
bool ok=false;

int        f(int v,int s,int l)
{
        int i;

           if(s==n)
           {
                   if(ok==false)
                {
                        ok=true;
                        ans[0]=v-1;
                        for(i=1;i<v;i++)
                                ans[i]=rez[i];
                }
                else
                        if(v-1<ans[0])
                        {
                                ans[0]=v-1;
                                for(i=1;i<v;i++)
                                        ans[i]=rez[i];
                        }
           }
           else
           {
                   for(i=l;i<=m;i++)
                           if(s+a[i]<=n)
                                   if(b[i]>0)
                                   {
                                           rez[v]=a[i];
                                           b[i]-=1;
                                           f(v+1,s+a[i],i);
                                           b[i]+=1;
                                   }
           }

        return 0;
}

int main()
{
        freopen("coins.in", "r", stdin);
        freopen("coins.out", "w", stdout);
        int s=0,i;

        cin>>n>>m;
        for(i=1;i<=m;i++)
        {
                cin>>a[i];
                b[i]=2;
                s+=a[i];
        }

        if(2*s<n) cout<<"-1";
        else
        {
                f(1,0,1);
                if(ok==false) cout<<"0";
                else
                {
                        cout<<ans[0]<<endl;
                        for(i=1;i<=ans[0];i++)
                                cout<<ans[i]<<" ";
                }
        }

        return 0;
}
