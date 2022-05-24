from curses.ascii import isalnum, isdigit

# input file
f1 = open('ZJ.dat', mode='r', encoding='gbk')
# output file
f2 = open('res.txt', mode='w+', encoding='gbk')
i = 0
temp1 = set()
temp2 = set()
voltage = set()

for line in f1:
    i += 1
    # if not data row, no need to convert 
    if len(line) == 0 or line[0] == '.':
        # f2.write(line)
        pass
    elif not 'A' <= line[0] <= 'Z':
        # speical case, line 924 is an empty line
        # f2.write(line)
        pass
    else:
        if (isalnum(line[9]) or line[9] == '-' or line[9] == '_'):
            # English word, voltage starts from line[11]
            j = 11
            temp1.add(line[11])
            if not isdigit(line[11]):
                f2.write("line " + str(i) + '\n')
                f2.write(line)
        else:
            # chinese word, voltage starts from line[10]
            j = 10
            temp1.add(line[10])
            if not isdigit(line[10]):
                f2.write("line" + str(i))
                f2.write(line)
        volt = ""
        while not isdigit(line[j]):
            volt += line[j]
            j += 1
        voltage.add(volt) 
        # temp1.add(line[9])
        # temp2.add(line[10])


f1.close()
f2.close()

print("===================voltage=======================")
for v in voltage:
    print(v)

print("===================temp1=========================")
for i in temp1:
    print(i, isalnum(i) or i == '-' or i == '_')
print("===================temp2=========================")
for i in temp2:
    print(i, isalnum(i) or i == '-' or i == '_')
            
        