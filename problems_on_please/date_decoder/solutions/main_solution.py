#!/usr/bin/python3
def date_formatter(string, months):
    
    string_splitted = string.split("-")
    day = string_splitted[0]
    month = months[string_splitted[1]]

    year = string_splitted[2]
    if len(year) < 2:
        year = "0" + year
        
    if int(year) < 50:
        year = "20" + year
    else:
        year = "19" + year
        
    return (year, month, day)



input_file = open('date_decoder.in', "r")
output_file = open('date_decoder.out', "w")

input_string = input_file.readline().rstrip()
months = {"JAN":1, "FEB":2, "MAR":3, "APR":4, "MAY":5, "JUN":6, "JUL":7, "AUG":8, "SEP":9, "OCT":10, "NOV":11, "DEC":12}

(year, month, day) = date_formatter(input_string, months)
output_file.write(year + " " + str(month) + " " + day)
input_file.close()
output_file.close()