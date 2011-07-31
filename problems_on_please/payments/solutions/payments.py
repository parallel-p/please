def main () :
    input_file = open('payments.in',"r")
    output_file = open('payments.out', "w")
    names = []
    payments = []
    all_lines = input_file.readlines()
    for read_string in  all_lines :
        name, payment = read_string.split()
        if not name in names :
            names.append(name)
            payments.append(int(payment))
        else :
            payments[names.index(name)] += int(payment)

    for name in names :
        output_file.write(name + ' ' + str(payments[names.index(name)]) + '\n')
        
        
    input_file.close()
    output_file.close()

if __name__ == '__main__':
    main()
