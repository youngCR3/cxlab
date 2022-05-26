def isalpha(i):
    return (i >= 'a' and i <= 'z') or (i >= 'A' and i <= 'Z')

def isdigit(i):
    return i >= '0' and i <= '9'

def isalnum(i):
    return isalpha(i) or isdigit(i)

# input file
f1 = open('ZJ.dat', mode='r', encoding='gbk')
# output file
f2 = open('res.dat', mode='w+', encoding='gbk')
i = 0
temp1 = set()
temp2 = set()
voltage = set()

# Step1: find all the voltages
row = 0
for line in f1:
    row += 1
    # if not data row, no need to convert 
    if len(line) == 0 or line[0] == '.':
        pass
    elif not 'A' <= line[0] <= 'Z':
        # speical case, line 924 is an empty line
        pass
    else:
        start = 0
        if isalnum(line[9]) or line[9] == '-' or line[9] == '_':
            # English word, voltage starts from line[11]
            start = 11
        else:
            # chinese word, voltage starts from line[10]
            start = 10
        j = start
        volt = ""
        while isdigit(line[j]):
            volt += line[j]
            j += 1
        # special case: voltage is .69/.48/.32/.4 or situations like line 201
        if len(volt) > 0:
            voltage.add(volt) 
        if (line[0] == 'L' or line[0] == 'T') and line[1] == ' ':
            if start == 10:
                # 4-word name, voltage starts from line[20]
                j = 20
            else:
                # 3-word name, voltage starts from line[21]
                j = 21
            volt = ""
            while isdigit(line[j]):
                volt += line[j]
                j += 1
            if len(volt) > 0:
                voltage.add(volt)

# Step2: build voltage to chinese word map
words = "一二三四五六七八九十爱因斯坦牛顿居里夫人柯南道尔图灵吴朝晖特朗普萨拉赫科比阿诺德江博游"
wordsSet = set(i for i in words)
if len(words) != len(wordsSet):
    raise Exception("words has duplicate words")
voltage = [int(i) for i in voltage]
voltage.sort()
voltage = [str(i) for i in voltage]
voltage.append('.69')
voltage.append('.32')
voltage.append('.48')
voltage.append('.4')
voltage2Word = {}
if len(words) < len(voltage):
    raise Exception("words length cannot cover all voltages")
for i in range(len(voltage)):
    voltage2Word[voltage[i]] = words[i]

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
         
        if (line[0] == 'L' or line[0] == 'T') and line[1] == ' ':
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
            word1 = voltage2Word[volt]
            if start == 10:
                # 4-word name, voltage starts from line[20]
                j = 20
            else:
                # 3-word name, voltage starts from line[21]
                j = 21
            volt = ''
            if line[j] == '.':
                volt += '.'
                j += 1
            while isdigit(line[j]):
                volt += line[j]
                j += 1
            if volt not in voltage2Word:
                print(row)
                raise Exception("voltage " + volt + " not in voltage2Word") 
            word2 = voltage2Word[volt]
            replaceIndex = 15 if start == 10 else 16
            newLine = line[: 6] + word1 + line[7: replaceIndex] + word2 + line[replaceIndex + 1: ]
            f2.write(newLine)
            
        else:
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
        