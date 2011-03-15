#include <stdio.h>
int main()
{
    FILE* f = fopen("cpp_test", "w");
    fprintf(f, "9 8");
    fclose(f);
    return 0;
}