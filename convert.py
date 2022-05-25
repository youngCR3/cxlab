from curses.ascii import isalnum, isdigit

# input file
f1 = open('ZJ.dat', mode='r', encoding='gbk')
# output file
f2 = open('res.dat', mode='w+', encoding='gbk')
i = 0
temp1 = set()
temp2 = set()
voltage = set()

# Step1: find all the voltages
for line in f1:
    # if not data row, no need to convert 
    if len(line) == 0 or line[0] == '.':
        pass
    elif not 'A' <= line[0] <= 'Z':
        # speical case, line 924 is an empty line
        pass
    else:
        j = 0
        if (isalnum(line[9]) or line[9] == '-' or line[9] == '_'):
            # English word, voltage starts from line[11]
            j = 11
            if not isdigit(line[11]):
                # special case: voltage is .69/.48/.32/.4 or situations like line 201
                continue
        else:
            # chinese word, voltage starts from line[10]
            j = 10
            if not isdigit(line[10]):
                # special case: voltage is .69/.48/.32/.4 or situations like line 201
                continue
        volt = ""
        while isdigit(line[j]):
            volt += line[j]
            j += 1
        voltage.add(volt) 

# Step2: build voltage to chinese word map
words = "一二三四五六七八九十爱因斯坦牛顿居里夫人柯南道尔图灵吴朝晖特朗普萨拉赫科比阿诺德"
wordsSet = set(i for i in words)
if len(words) != len(wordsSet):
    raise Exception("words has duplicate words")
voltage = [int(i) for i in voltage]
voltage.sort()
voltage.append('.69')
voltage.append('.32')
voltage.append('.48')
voltage.append('.4')
voltage2Word = {}
if len(words) < len(voltage):
    raise Exception("words length cannot cover all voltages")
for i in range(len(voltage)):
    voltage2Word[str(voltage[i])] = words[i]

# ======================voltage2Word==========================
print(voltage2Word)
f1.close()
f1 = open('ZJ.dat', mode='r', encoding='gbk')
# Step3: convert
# replace the 3-word name with a voltage2word and 2-word name
row = 0
for line in f1:
    row += 1
    # if not data row, no need to convert 
    if len(line) == 0 or line[0] == '.':
        f2.write(line)
    elif not 'A' <= line[0] <= 'Z':
        # speical case, line 924 is an empty line
        f2.write(line)
    else:
        start = 0
        if (isalnum(line[9]) or line[9] == '-' or line[9] == '_'):
            # English word, voltage starts from line[11]
            start = 11
            if not isdigit(line[11]):
                # special case: voltage is .69/.32/.48/.4
                if len(line) > 12 and line[11] == '.' and isdigit(line[12]):
                    pass
                # special case: situations like line 201
                else:
                    f2.write(line)
                    continue
        else:
            # chinese word, voltage starts from line[10]
            start = 10
            if not isdigit(line[10]):
                # special case: voltage is .69/.32/.48/.4
                if len(line) > 11 and line[10] == '.' and isdigit(line[11]):
                    pass
                # special case: situations like line 201
                else:
                    f2.write(line)
                    continue
        volt = "" 
        j = 0
        if line[start] == '.':
            volt += '.'
            j = start + 1
        else:
            j = start
        while isdigit(line[j]):
            volt += line[j]
            j += 1
        if volt not in voltage2Word:
            print(row)
            raise Exception("voltage " + volt + " not in voltage2Word")
        word = voltage2Word[volt]
        newLine = line[: 6] + word + line[7: ]
        f2.write(newLine)

f1.close()
f2.close()

        