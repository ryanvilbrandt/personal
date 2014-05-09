def ascii2int(data, LSB=False, signed=False):
    if LSB: data = data[::-1]
    b = 0
    for c in data:
        b = (b<<8) + ord(c)
    if signed and (b & (1<<(8*len(data)-1))): # If MSB is a 1
        b -= (1<<(8*len(data)))
    return b

# If len(a) < length, will pad with leading nulls
def int2ascii(data, length, LSB=False):
    if data < 0:
        data += (1<<(8*length))
    a = ""
    while not data<=0:
        a = chr(data & 0xFF) + a
        data = data >> 8
    while len(a)<length: a = "\x00"+a
    if LSB: a = a[::-1]
    return a

def hex2int(data, LSB=True, signed=False):
    """
    Converts a space-separated string of hex values into an int
    @param data: A string of two-digit, space-separated hex values
    @param LSB: If True, leftmost hex value is the least significant byte
    @return int: Converted value of the hex string
    """
    data = data.split(' ')
    n = 0
    if not LSB: data.reverse()
    count = 0
    for i,x in enumerate(data):
        if x:
            count += 1
            n += (int(x,16) << (8*i))
    if signed and (n & (1<<(8*count-1))): # If MSB is a 1
        n -= (1<<(8*count))
    return n

def hex2ascii(data):
    """
    Converts a space-separated string of hex values into an ASCII string
    @param data: A string of two-digit, space-separated hex values
    @return str: Converted string
    """
    return "".join([chr(int(c,16)) for c in data.split(' ')
                    if c])

def getint(s, length):
    return hex2int(s[:length*3]),s[length*3:]

def getascii(s, length=0):
    if length:
        temp = s[:length*3].find('00')
        return hex2ascii(s[:temp]),s[length*3:]
    else:
        temp = s.find('00')
        return hex2ascii(s[:temp]),s[temp+3:]

print repr(int2ascii(1,2,LSB=True)+int2ascii(338378,4,LSB=True))
##print ascii2int('S\x00')
##print repr(int2ascii(-32768,2))
##print hex2int('52 0F')
print "Press Ctrl+C to exit..."
print ""
try:
    while True:
        print hex2int(raw_input(), signed=True)
        print ""
except KeyboardInterrupt:
    print "Exitting..."

##a = ['1.30','10.00\xb8\x9d\x03','30.00Za\x03','1.00','0.15','60','0',u'18000\xb3U\x03','0','0','2']
##
##gps_data = [x[:-3] if (x[-1] == '\x03') else x
##            for x in a]
##print gps_data

