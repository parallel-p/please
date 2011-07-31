#include <iostream>
#include <map>
#include <iostream>
#include <cstring>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <stdio.h>

using namespace std;

int str2int(string s)
{
	stringstream ss(s);
	int result;
	return ss >> result ? result : 0;
}

int main () 
{	
	freopen("date_decoder.out", "w", stdout);
	freopen("date_decoder.in", "r", stdin);
	
    string str;
    cin >> str;
	
	vector<string> splitted;

	int found;
    found = str.find_first_of("-");
    while (found != string::npos){
        if (found > 0){
            splitted.push_back(str.substr(0,found));
        }
        str = str.substr(found+1);
        found = str.find_first_of("-");
    }
    if(str.length() > 0){
        splitted.push_back(str);
    }
	
	map <string, string> months;
	months["JAN"] = "1";
	months["FEB"] = "2";
	months["MAR"] = "3";
	months["APR"] = "4";
	months["MAY"] = "5";
	months["JUN"] = "6";
	months["JUL"] = "7";
	months["AUG"] = "8";
	months["SEP"] = "9";
	months["OCT"] = "10";
	months["NOV"] = "11";
	months["DEC"] = "12";
	
	string day_s = splitted.at(0);
	string month_s = splitted.at(1);
	string year_s = splitted.at(2);
	
	int year = str2int(year_s);
	if (year_s.length() < 2) {
		cout << "200" << year_s;
	} else {
		if (year > 49) {
			cout << "19" << year_s;
		} else {
			cout << "20" << year_s;
		}
	}
	
	cout << " " << months[month_s] << " " << day_s;
    return 0;
}
