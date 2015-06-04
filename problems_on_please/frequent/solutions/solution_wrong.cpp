#include <iostream>
#include <memory.h>
#include <cstdio>
#include <cstdlib>
#include <cmath>
using namespace std;
bool is_capital(char c ){
     return ((c > 'A') && (c <= 'Z'));
}
bool is_small(char c ){
     return ((c >= 'a' ) && (c < 'z'));
}
int main () {
     int small[30];
     int capital[30];
     memset(small,0,sizeof(small));
     memset(capital,0,sizeof(capital));
     char c = 'a';
     while (scanf("%c",&c) == 1){
           if (is_capital(c)){
               capital[c-'A']++;
           }
           if (is_small(c)){
               small[c-'a']++;
           }
     }
     int maxnum = 0;
     char best;
     for (int i = 0;i < 30;i++){
         if (capital[i] > maxnum){
             maxnum = capital[i];
             best = 'A'+i;
         }
     }
     for (int i = 0;i < 30;i++){
         if (small[i] > maxnum){
             maxnum = small[i];
             best = 'a'+i;
         }
     }

     cout << best;
}
