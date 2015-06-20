"""
Serial connection tunnel
@author Ryan Vilbrandt
@version 1.0.0

Provides a bridge between two serial ports, allowing two hardware
devices to talk to each other, while logging all communication between them.
"""
import serial, sys, time, threading
from struct import unpack

REPR, Hex, HEX, oldhex, FANCY = 0, 1, 2, 3, 4
FANCY_LENGTH = 24

PORT1 = "COM4"
PORT2 = "COM8"
BAUD = 38400
TIMEOUT = 0.02
MODE = FANCY
TIMESTAMP = False
parsed_string = ""

PACKETS = {
   0x0A: "GetDevId",
   0x25: "GenData",
   0x27: "TagEvent",
   0x33: "ZPass",
   0x37: "DevPhoneHomeResponse?",
   0x8A: "GetDevIdRet",
   0xA5: "GenDataRet",
   0xA7: "TagEventRet",
   0xA8: "GetPositionRet",
   0xB3: "ZPassRet",
   0xB7: "AllDevPhoneHome",
   }

DEVICE_IDS = {
   0x04: "GPS",
   0x0B: "ZPass",
   0xFF: "Broadcast"
   }

ZPASS_OPS = {
   0: "RequestTime",
   1: "RequestGpsUpdate",
   2: "RequestAppInfo",
   3: "RequestDeleteData",
   4: "RequestPhoneHome",
   5: "RequestResetSleepCounter",
   6: "RequestReboot",
   128: "ResponseTime",
   129: "ResponseGpsUpdate",
   130: "ResponseAppInfo",
   131: "ResponseDeleteData",
   132: "ResponsePhoneHome",
   133: "ResponseResetSleepCounter",
   134: "ResponseReboot",
   }

class SerialEndpoint():

   stop_threads = False
   is_alive = False

   def __init__(self, port_name):
      self.port_name = port_name

   def StartThread(self, read_port, write_port):
      '''
      @param Serial read_port: An open port to be read from
      @param Serial write_port: An open port to be written to
      '''
      t = threading.Thread(name=self.port_name, target=self.RunPort,
                           args=[read_port, write_port])
      t.start()

   def RunPort(self, read_port, write_port):
      self.stop_threads = False
      self.is_alive = True
      newline = False
      try:
         while not self.stop_threads:
            serial_data = self.ReadFromPort(read_port)
            if serial_data:
               self.SendSerialData(write_port, serial_data)
               # Quick hack to split multiple packets
               serial_data = serial_data.replace('\x03\x02\x03', '\x03SPLITME\x02\x03')
               serial_data_list = serial_data.split('SPLITME')
               for s in serial_data_list:
                  self.PrintSerialData(s)
      except Exception as e:
         print "Exception in thread {}\n{}".format(self.port_name, e)
      self.ClosePort(read_port)
      self.is_alive = False
   
   def OpenPort(self, baud=38400, timeout=0.02):
      try:
         return serial.Serial(self.port_name, BAUD, timeout=TIMEOUT)
      except serial.SerialException as e:
         print "Error when opening port {}: {}".format(self.port_name, e)
         self.stop_threads = True
         return None

   def ClosePort(self, port):
      try:
         port.close()
      except Exception:
         pass

   def ReadFromPort(self, port):
      return port.readall()

   def SendSerialData(self, port, data):
      port.write(data)

   def PrintSerialData(self, string):
      '''
      A helper function for printing the serial data in a more readable format
      '''
      # Begin with port name
      out_string = "{}\n".format(self.port_name)
      # Set a timestamp
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
                  parsed_string += c
               else:
                  parsed_string += "."
            # Convert raw data like in the HEX section
            out_raw_data = " ".join(["{0:02x}".format(ord(c)) for c in current_data])
            out_string += out_raw_data
            # Padding, if this line of the raw_data doesn't fill its whole section
            out_string += max(0, " "*(FANCY_LENGTH*3-len(out_raw_data)))
            out_string += "   "
            # Add parsed string
            out_string += parsed_string
            out_string += "\n"
            # Set next data to process
            current_data = next_data[:FANCY_LENGTH]
            next_data = next_data[FANCY_LENGTH:]
      # End with a new line and print to console
      out_string += self.ParseZPacket(string)
      # Manually add new line so that print cannot be interupted before newline
      out_string += "\n"
      print out_string,

   def ParseZPacket(self, string):
      if not (string.startswith('\x02\x03') and string.endswith('\x03')):
         return ""
      output_string = ""
      packet, source, target = [ord(c) for c in string[4:7]]
      output_string += "Packet: {: <20}Source: {: <10}Target: {}\n".format(
         PACKETS.get(packet, hex(packet)),
         DEVICE_IDS.get(source, hex(source)),
         DEVICE_IDS.get(target, hex(target)),
         )
      if packet in (0x0A, 0x25, 0xA5, 0xB7):  # GetDevId, GenData, GenData Ret, AllDevPhoneHome
         pass
      elif packet == 0x27:  # TagEvent
         message_version = ord(string[7])
         operation = ord(string[8])
         payload = string[9:-3]
         params = [str(unpack("<I", payload[i:i+4])[0]) for i in xrange(0, 24, 4)]
         entry_count = ord(payload[24])
         tag_data = repr(payload[25:])
         output_string += "Message version: {}\tOperation: {}\n".format(
            message_version, operation
            )
         output_string += "Params: {}\tEntry count: {}\tTag data: {}\n".format(
            " ".join(params), entry_count, tag_data
            )
      elif packet == 0x33:  # ZPass
         message_version = ord(string[7])
         operation = ZPASS_OPS.get(ord(string[8]), ord(string[8]))
         payload = string[9:-3]
         output_string += "Message version: {}\tOperation: {}\tPayload: {!r}\n".format(
            message_version, operation, payload
            )
      elif packet == 0x8A:  # GetDevIdRet
         output_string += "GPSID: {}\n".format(unpack("<I", string[7:11])[0])
      elif packet in (0xA7, 0xA8):  # TagEventRet, GetPositionRet
         gpsid = unpack("<I", string[7:11])[0]
         payload = string[7:-3]
         output_string += "GPSID: {}\tPayload: {!r}\n".format(gpsid, payload)
      elif packet == 0xB3:  # ZPassRet
         gpsid = unpack("<I", string[7:11])[0]
         message_version = ord(string[11])
         operation = ZPASS_OPS.get(ord(string[12]), ord(string[12]))
         payload = string[13:-3]
         output_string += "GPSID: {}\tMessage version: {}\tOperation: {}\n".format(
            gpsid, message_version, operation
            )
         output_string += "Payload: {!r}\n".format(payload)
      else:
         pass
      return output_string
      
      

def SetUpEndpoints(port_name1, port_name2):
   print "Opening port {}".format(port_name1)
   endpoint1 = SerialEndpoint(port_name1)
   port1 = endpoint1.OpenPort()
   if port1 is None:
      return None, None
   print "Opening port {}".format(port_name2)
   endpoint2 = SerialEndpoint(port_name2)
   port2 = endpoint2.OpenPort()
   if port2 is None:
      endpoint1.ClosePort(port1)
      return None, None
   endpoint1.StartThread(port1, port2)
   endpoint2.StartThread(port2, port1)
   return endpoint1, endpoint2

endpoints = SetUpEndpoints(PORT1, PORT2)

if all(endpoints):
   print "Running, press Ctrl+C to break"
   try:
      while(True):
         time.sleep(1)
   except KeyboardInterrupt:
      print ""
      print "Exitting..."

   for e in endpoints:
      e.stop_threads = True

   while True:
      any_alive = [e.is_alive for e in endpoints]
##      print any_alive
      if not any(any_alive):
         break
      time.sleep(0.1)
   print "Done."
