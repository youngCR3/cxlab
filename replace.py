from json import encoder

# input file
f1 = open('ZJ.dat', encoding='gbk')
# output file
f2 = open('res.dat', mode='w+', encoding='gbk')
i = 0
for line in f1:
    line1 = []
    count = 0
    for i in line:
        if i == '_':
            if count == 0:
                count += 1
            elif count == 1:
                count += 1
            else:
                count = 0
        else:
            if count == 2:
                count += 1
            elif count == 3:
                count += 1
            else:
                count = 0
        line1.append(i)
        if count == 4:
            line1[-4] = line1[-2]
            line1[-3] = line1[-1]
    s = ''.join(line1)
    f2.write(s)
f1.close()
f2.close()
            
        