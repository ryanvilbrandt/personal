temp_s = "[setq(p,0|0|0|0|0|0|-4|-2|-1|0|1|2|3|5|7|10|13|17)][ljust([defansi(BRIGHT,Points:)]%b[switch(setr(0,ladd(iter(get(%qn/_A.ATTRIBUTES.LEVEL1),elements(%qp,after(##,@),|),|))),32,%xh%xg%q0%xn,%xh%xr%q0%xn)],15)]"

def IsNewLine(s):
    for c in s[::-1]:
        if c == "\n":
            return True
        elif not c == " " or c == "\t":
            return False
        else:
            return True
          

s = ""
level = 0
skip = False
tab = " "*4
for c in temp_s:
    if skip:
        s += c
        skip = False
    else:
        if c == '\\' or c == '%':
            s += c
            skip = True
        elif c == '(':
            level += 1
            s += c+'\n'+tab*level
        elif c == ',':
            s += c+'\n'+tab*level
        elif c == ')':
            level -= 1
            s += '\n'+tab*level+c
        elif c == '[' and len(s) > 0:
            if not IsNewLine(s):
                s += '\n'+tab*level+c
            else:
                s += c
        else:
            s += c

print "-----"
print s
