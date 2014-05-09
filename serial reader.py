"""
@author Ryan Vilbrandt
@version 1.0.3
"""


import serial, sys, time

REPR, Hex, HEX, oldhex, FANCY = 0, 1, 2, 3, 4
FANCY_LENGTH = 16

PORT = 45
BAUD = 9600
TIMEOUT = 0.02
MODE = FANCY
TIMESTAMP = False
parsed_string = ""

try:
   s = serial.Serial("COM{0}".format(PORT), BAUD, timeout=TIMEOUT)
except serial.SerialException as e:
   print e
   PORT = raw_input("COM port? ")
   s = serial.Serial("COM{0}".format(PORT), BAUD, timeout=TIMEOUT)

##s.write('\x02\x03\x0A\x00\x23\x06\x04\xD7\x2C\x03')

print "Running, press Ctrl+C to break"
newline = False
try:
   while(True):
      string = s.read(1)
      if string:
         if not newline and TIMESTAMP:
            sys.stdout.write("["+time.ctime()+"] ")
         if MODE == REPR:
            sys.stdout.write("{0!r}".format(string).strip("'"))
         elif MODE == Hex:
            sys.stdout.write("{0:02x}".format(ord(string))+' ')
         elif MODE == HEX:
            sys.stdout.write("{0:02X}".format(ord(string))+' ')
         elif MODE == oldhex:
            sys.stdout.write(hex(ord(string))+' ')
         elif MODE == FANCY:
            sys.stdout.write("{0:02X}".format(ord(string))+' ')
            if len(repr(string)) == 3:
               parsed_string += string
            else:
               parsed_string += "."
            if len(parsed_string) >= FANCY_LENGTH:
               print "  "+parsed_string
               parsed_string = ""
         newline = True
      else:
         if newline:
            if MODE == FANCY and parsed_string:
               print " "*3*(FANCY_LENGTH-len(parsed_string))+"  "+parsed_string
               parsed_string = ""
            print ""
            newline = False
##         time.sleep(0.1)
except KeyboardInterrupt:
   print ""
   print "Exitting..."
##   s.write(' ')

s.close()
