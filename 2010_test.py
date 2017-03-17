import serial, time

s = serial.Serial("COM8", 38400, timeout=1)

print "Writing to 2010"
# s.write("\x02\x73\x49\x5A\x03")
# s.write("\x02\x67\x46\x03")
s.write("\x02\x67\x68\x03")
# s.write("help\r")
print "Reading..."

try:
    out = ""
    while True:
        r = s.read(1)
        out += r
        if r == '':
            print repr(out)
            break
    print "Done"
except KeyboardInterrupt:
    print "Aborting..."

s.close()
