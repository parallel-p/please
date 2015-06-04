#include <fstream>

using namespace std;

int main()
{    
	ifstream in("keyvalue.in");
	ofstream out("keyvalue.out");
	
	int number = 0; in >> number;	
	
	string text((istreambuf_iterator<char>(in)), istreambuf_iterator<char>());				 
	
	// Skip all lines before the line we need
	int cur_line = 0;
	int i = 1;
	while(i < text.size() && cur_line != number - 1)	
	{
		if (text[i] == '\n')
		{
			cur_line++;
		}
		i++;
	}
	
	
	
	// Skip key[number] = 
	while(text[i] != '\0' && text[i] != '=') i++;
	i += 2;
	
	// Print value
	while(text[i] != '\0')
	{
		out << text[i++];
	}
	
	in.close();
	out.close();	
    return 0;
}