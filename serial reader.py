"""
@author Ryan Vilbrandt
@version 1.0.3
"""


import serial, sys, time

REPR, Hex, HEX, oldhex, FANCY = 0, 1, 2, 3, 4
FANCY_LENGTH = 16

PORT = 3
BAUD = 38400
TIMEOUT = 0.02
MODE = REPR
TIMESTAMP = False
parsed_string = ""

try:
   s = serial.Serial("COM{0}".format(PORT), BAUD, timeout=TIMEOUT)
except serial.SerialException as e:
   print e
   PORT = raw_input("COM port? ")
   s = serial.Serial("COM{0}".format(PORT), BAUD, timeout=TIMEOUT)

##s.write('\x02\x03\x0A\x00\x23\x06\x04\xD7\x2C\x03')

def ReadFromPort(port):
   return port.readall()

def PrintSerialData(string):
   '''
   A helper function for printing the serial data in a more readable format
   '''
   # Set a timestamp
   out_string = ""
   if TIMESTAMP:
      out_string += "["+time.ctime()+"] "
   # Print out code using repr()
   if MODE == REPR:
      out_string += repr(string).strip("'")
   # Convert every character to its 2-digit hex representation
   # Space separated. Does not support unicode
   elif MODE in (Hex, HEX):
      data = " ".join(["{0:02x}".format(ord(c)) for c in string])
      # Cast to upper case
      if MODE == HEX:
         data = data.upper()
      out_string += data
   # Convert every character to its 2-digit hex representation
   # And provide a translation on the right side, like seen in most
   # serial port monitors. Any unprintable characters will be printed
   # as periods.
   elif MODE == FANCY:
      # Split the data into chunks, based on how wide the
      # "raw data" section should be.
      current_data = string[:FANCY_LENGTH]
      next_data = string[FANCY_LENGTH:]
      # While there's still raw data to parse, keep going
      while current_data:
         parsed_string = ""
         # For each character in the parsed data, try to convert it
         # with repr(). If the result is three characters long like 'X'
         # Then it's a printable character. Otherwise, use a period.
         for c in current_data:
            if len(repr(c)) == 3:
               parsed_string += string
            else:
               parsed_string += "."
         # Convert raw data like in the HEX section
         out_raw_data = " ".join(["{0:02x}".format(ord(c)) for c in string])
         out_string += out_raw_data
         # Padding, if this line of the raw_data doesn't fill its whole section
         out_string += max(0, " "*(FANCY_LENGTH-len(out_raw_data)))
         out_string += "   "
         # Add parsed string
         out_string += parsed_string
         out_string += "\n"
   # End with a new line and print to console
   out_string += "\n"
   print out_string

print "Running, press Ctrl+C to break"
newline = False
try:
   while(True):
      string = ReadFromPort(s)
      if string:
         PrintSerialData(string)
##      string = s.read(1)
##      if string:
##         if not newline and TIMESTAMP:
##            sys.stdout.write("["+time.ctime()+"] ")
##         if MODE == REPR:
##            sys.stdout.write("{0!r}".format(string).strip("'"))
##         elif MODE == Hex:
##            sys.stdout.write("{0:02x}".format(ord(string))+' ')
##         elif MODE == HEX:
##            sys.stdout.write("{0:02X}".format(ord(string))+' ')
##         elif MODE == oldhex:
##            sys.stdout.write(hex(ord(string))+' ')
##         elif MODE == FANCY:
##            sys.stdout.write("{0:02X}".format(ord(string))+' ')
##            if len(repr(string)) == 3:
##               parsed_string += string
##            else:
##               parsed_string += "."
##            if len(parsed_string) >= FANCY_LENGTH:
##               print "  "+parsed_string
##               parsed_string = ""
##         newline = True
##      else:
##         if newline:
##            if MODE == FANCY and parsed_string:
##               print " "*3*(FANCY_LENGTH-len(parsed_string))+"  "+parsed_string
##               parsed_string = ""
##            print ""
##            newline = False
##         time.sleep(0.1)
except KeyboardInterrupt:
   print ""
   print "Exitting..."
##   s.write(' ')

s.close()
