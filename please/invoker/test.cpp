#include <iostream>
#include <stdlib.h>
#include <ctime>
using namespace std;

int main(int argc, char* argv[])
{
    if (argc == 1) 
         return 42;
    
    double tl = atof(argv[1]);
    double ml = atof(argv[2]) * (1 << 20);
    
    char *p_array = new char[(int)(ml)];
    
    p_array[0] = p_array[1] = 1;
    for(int i = 2; i < ml; i++)
        p_array[i] = p_array[i - 1] + p_array[i - 2];
    
    while(clock() < tl * CLOCKS_PER_SEC);
    
    delete (p_array);
    
    return 0;
}

