import serial, sys, time

PORT = 15
REPR, Hex, HEX, oldhex = 0, 1, 2, 3
MODE = HEX

try:
   s = serial.Serial("COM{0}".format(PORT), 115200, timeout=0.5)
except serial.SerialException as e:
   print e
   PORT = raw_input("COM port? ")
   s = serial.Serial("COM{0}".format(PORT), 115200, timeout=0.5)

prompt = raw_input("Config? ")
if prompt.lower().startswith('y'):
   s.flushInput()
   s.flushOutput()
   print ""
##   s.write('?\r')
##   for l in s.readlines(): sys.stdout.write(l)
   s.write('m\r') # Change mode
   s.write('3\r') # UART
   s.write('7\r') # 38400 baud
   s.write('1\r') # 8 bit, NONE
   s.write('1\r') # Stop bits: 1
   s.write('1\r') # 1 = Idle 1, 2 = Idle 0
   s.write('1\r') # Open Drain (HI-Z)
##   for l in s.readlines(): sys.stdout.write(l)

s.write('(2)\r')
##inp = raw_input('>>>')
##s.write(inp+'\r')
time.sleep(1)
s.flushInput()
s.flushOutput()

print "Reading Raw input..."
newline = False
try:
   while(True):
      string = s.read(1)
      if string:
         if MODE == REPR:
            sys.stdout.write(repr(string).strip("'"))
         elif MODE == Hex:
            sys.stdout.write("{0:02x}".format(ord(string))+' ')
         elif MODE == HEX:
            sys.stdout.write("{0:02X}".format(ord(string))+' ')
         elif MODE == oldhex:
            sys.stdout.write(hex(ord(string))+' ')
         newline = True
      elif newline:
            print ""
            newline = False
except KeyboardInterrupt:
   print ""
   print "Exitting..."
   s.write(' ')

s.close()
