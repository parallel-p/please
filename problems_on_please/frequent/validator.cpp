#include "testlib.h"

using namespace std;
bool is_capital(char c){
     return ((c >= 'A') && (c <= 'Z'));
}
bool is_small(char c){
     return ((c >= 'a') && (c <= 'z'));
}
const int MAXCHARNUM = 1000000;
int main() {
    registerValidation();
    int counter = 0;
    while (!inf.eof()){
        char c = inf.readChar();
        counter++;
        if ((!is_capital(c))&&(!is_small(c))&&(c != ' ')&&(c != '\n')&&(c!='\r')){
             quitf(_fail, "test is invalid");
        }
        if (counter > MAXCHARNUM)
             quitf(_fail, "test is too big");
    }
    return 0;  
}