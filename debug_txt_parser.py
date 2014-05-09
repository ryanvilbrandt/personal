import time, re

with open("debug 010 - Copy2.txt", 'r') as f:
    s = f.read()
    
lines = s.split('\n')
##print repr(lines[0:10])

count = 0
test_lines = []
for i,_ in enumerate(lines):
    if _ == "Summary: All tests passed":
        a = eval(lines[i-1])
        n = float(lines[i-2].split(' ')[0])
##        print n
        new_a = [time.strftime("%m/%d/2012 %H:%M",time.gmtime(n))]
        new_a.append(re.search('(.+?),Pass', a[26]).group(1))
        try:
            new_a.append(re.search('(.+?) - Programmed,Pass', a[4]).group(1))
        except AttributeError:
            new_a.append(re.search('(.+?),Pass', a[4]).group(1))
        new_a.append(re.search('(.+?),Pass', a[22]).group(1))
        new_a.append(re.search('Connected - (.+?),Pass', a[0]).group(1))
        test_lines.append(new_a)

print len(test_lines)
##print test_lines[0]
##print test_lines

s = ""
for _ in test_lines:
    s += ",".join(_[0:3])
    s += ",'{0}',{1},\n".format(_[3],_[4])

with open("output.csv","w") as f:
    f.write(s)
