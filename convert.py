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
    if len(line) >= 0 and line[0] == 'D' and line[1] == 'C':
        continue
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
        volt = line[j: j + 4]
        voltage.add(volt) 
        if line[0] == 'L' or line[0] == 'T' or line[0] == 'R':
            if start == 10:
                # 4-word name, voltage starts from line[20]
                j = 20
            else:
                # 3-word name, voltage starts from line[21]
                j = 21
            volt = line[j: j + 4]
            voltage.add(volt)

# Step2: build voltage to chinese word map
words = "一二三四五六七八九十爱因斯坦牛顿居里夫人柯南道尔图灵吴朝晖特朗普萨拉赫科比阿诺德江博游"
wordsSet = set(i for i in words)
if len(words) != len(wordsSet):
    raise Exception("words has duplicate words")
voltage = list(voltage)
voltage.sort()
voltage2Word = {}
if len(words) < len(voltage):
    print(voltage)
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
    if len(line) >= 0 and line[0] == 'D' and line[1] == 'C':
        continue
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
        else:
            # chinese word, voltage starts from line[10]
            start = 10
         
        if line[0] == 'L' or line[0] == 'T' or line[0] == 'R':
            j = start
            volt = line[j: j + 4]
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
            volt = line[j: j + 4]
            if volt not in voltage2Word:
                print(row)
                raise Exception("voltage " + volt + " not in voltage2Word") 
            word2 = voltage2Word[volt]
            replaceIndex = 15 if start == 10 else 16
            newLine = line[: 6] + word1 + line[7: replaceIndex] + word2 + line[replaceIndex + 1: ]
            f2.write(newLine)
            
        else:
            volt = line[start: start + 4]
            if volt not in voltage2Word:
                print(row)
                raise Exception("voltage " + volt + " not in voltage2Word")
            word = voltage2Word[volt]
            newLine = line[: 6] + word + line[7: ]
            f2.write(newLine)

f1.close()
f2.close()
        