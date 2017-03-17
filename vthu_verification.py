import time
import serial   # http://pyserial.sourceforge.net/
import J3Functions as j3

d = {11: "2029",
     12: "0",
     13: "0",
     15: "3",
     27: "1000",
     32: "57",
     3330: "3600000",
     3332: "0",
     7953: "120",
     7984: "1004",
     8012: "80",
     8080: "0",
     8094: "0"
     }

def encode_msg(msg):
    return [chr(int(c, 16)) for c in msg.split(' ')]

def send_message(port, msg, wait_for_response=True):
    pass

verify_conf_11 = "02 03 0C 00 18 06 04 0B 00 DF 65 03"

print