#include "testlib_mac.h"

int main() 
{
    registerValidation();
    int n = 0;
    n = inf.readInt(1 , 10000);
    inf.nextLine();
    for (int i = 0; i < n; i++) 
    {
        inf.readString();
        //inf.nextLine();
        inf.readString();
        //inf.nextLine();
    }
    inf.readLine();
    return 0;
}
