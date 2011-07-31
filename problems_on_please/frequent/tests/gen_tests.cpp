#include <cstdio>
#include <cassert>
#include <cstdlib>
#include <time.h>
#include <iostream>
using namespace std;
int mabs (int i){
   if (i < 0)
       return -i;
   return i;
}
int main (int argc, char **argv ){
     assert(argc == 4);
     srand (atoi(argv[3]));
     int line_number = atoi(argv[1]);
     int max_line_length = atoi(argv[2]);
     for (int i = 0; i < line_number;i++){
          int len = mabs(rand()%max_line_length);
          for (int i = 0;i < len;i++){
               int type = mabs(rand()%3);
               if (type == 0)
                  cout << " ";
               else if (type == 1){
                    int sdv = mabs(rand()%24);
                    cout << char ('a'+sdv);
               }
               else if (type == 2){
                    int sdv = mabs(rand()%24);
                    cout << char('A'+sdv);
               }
          }
          cout <<endl;
     }     
     return 0;
}