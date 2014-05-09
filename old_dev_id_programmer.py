import serial, threading, time
from struct import pack, unpack

DEBUG = False

port_name = "COM11"
BAUD = 9600

PACKET_VERSION = '\x03'
HEADER_VERSION = '\x01'

# Packet types
PTYPE_ZCON          = '\x34'
PTYPE_ZCON_MOBILE   = '\xB4'

# Device IDs
DEVICE_GPS              = '\x04'
DEVICE_PC               = '\x06'
DEVICE_J3               = '\x09'
DEVICE_ZCONMD           = '\x0C'
DEVICE_ZCONMDR          = '\x0D'
DEVICE_ZCONP            = '\x0E'
DEVICE_ZCONPR           = '\x0F'
DEVICE_ZCON_RESERVED    = '\x10'
DEVICE_ZCON_TR          = '\x11'
DEVICE_ZCONMDP          = '\x12'

# Operations
OP_PUMP_DATA    = '\x00'
OP_TRAILER_ID   = '\x01'
OP_DEVICE_INFO  = '\x02'
OP_JOIN_ID      = '\x03'
OP_RESET        = '\x04'
OP_PING         = '\x05'
OP_PHY_ADDR     = '\x06'
OP_RSSI         = '\x07'
OP_TRUCK_INFO   = '\x08'
OP_PROV         = '\x09'

# Actions
ACTION_SET      = '\x00'
ACTION_GET      = '\x01'
ACTION_ACK      = '\x02'
ACTION_RESET    = '\x03'
ACTION_NO_ACK   = '\x04'

# ZCON Prov operations
PROV_IR_DATA_SENT   = '\x00'

def J3Run(port, gps, vehicle_data):
    vehicle_message = CreateJ3Message(OP_PUMP_DATA, ACTION_SET, vehicle_data, gps=gps)
    ping_message = CreateJ3Message(OP_PING, ACTION_ACK, gps=gps)       # Build V2J messages now, for speed
    last_msg = ""
    
    while RunThreads:                            # Loop infinitely until the test ends
        msg = ReadJ3Message(port)
        if msg:
            op = msg[2]
            action = msg[3]
            if op == OP_PUMP_DATA and action == ACTION_GET:
                port.write(vehicle_message)
                last_msg = vehicle_message
            elif op == OP_PING and action == ACTION_GET:
                port.write(ping_message)
                last_msg = ping_message
            elif action == ACTION_ACK:
                pass
            elif action == ACTION_NO_ACK:
                port.write(last_msg)
            else:
                print "Unknown message", repr(op), repr(action)

    port.flushInput()                                                       # Thread is ending 
    port.flushOutput()
    print "J3 thread stopped"

def ReadJ3Message(port):
    try:
        line = port.read(1)                                             # Read next character from the serial port
    except serial.SerialException as e:
        line = ""                                                       # If something stupid happens to the Truck board, fail gracefully
    
    if DEBUG: print repr(line)
    if line == '\x02' and port.read(1) == PACKET_VERSION:               # If the next two characters are '\x02\x03', we have a valid message
        packet = '\x02' + PACKET_VERSION + port.read(2)                 # Grab the length bytes and read out the rest of the message

        length = unpack("<H", packet[2:4])[0]
        packet += port.read(length-4)
                                                                        # If the CRC is incorrect, ignore this packet
        if unpack("<H", packet[-3:-1])[0] == CalcCRC16(packet[:-3]):
            source = packet[5]                                          # Get source and target
            target = packet[6]
            
            op = packet[8]                                              # Get the ops+payload from the packet
            action = packet[9]
            payload = packet[10:-3]
            if DEBUG: print "{0!r}|{1!r}|{2!r}|{3!r}|{4!r}|{5!r}".format(packet,source,target,op,action,payload)
            return (source, target, op, action, payload)
        elif DEBUG: print "Bad CRC:",repr(packet)
            
    
    return None

def CreateJ3Message(op, action, payload="", ptype=PTYPE_ZCON_MOBILE, 
                    source=DEVICE_J3, target=DEVICE_ZCONP, gps=0x00):
    # If no GPS, don't try to pack. It'll throw an Exception
    if type(gps) is int: gps = pack("<I",gps)
    # Prepend header
    out = "{0}{1}{2}{3}{4}{5}{6}{7}".format(ptype,
                                            source,
                                            target,
                                            gps,
                                            HEADER_VERSION,
                                            op,
                                            action,
                                            payload)
    # Prepend start bytes and length
    out = "\x02" + PACKET_VERSION + pack("<H",7+len(out)) + out
    # Append CRC and stop byte, and return
    sent = out + pack("<H", CalcCRC16(out)) + '\x03'
    if DEBUG: print "Message built:",repr(sent)
    return sent

## reversed crc algoithm, crc must start out at 0xFFFF */
def CalcCRC16(data):
    ccitt_16 = (0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50A5, 0x60C6, 0x70E7, 0x8108, 0x9129, 0xA14A, 
            0xB16B, 0xC18C, 0xD1AD, 0xE1CE, 0xF1EF, 0x1231, 0x0210, 0x3273, 0x2252, 0x52B5, 0x4294, 
            0x72F7, 0x62D6, 0x9339, 0x8318, 0xB37B, 0xA35A, 0xD3BD, 0xC39C, 0xF3FF, 0xE3DE, 0x2462, 
            0x3443, 0x0420, 0x1401, 0x64E6, 0x74C7, 0x44A4, 0x5485, 0xA56A, 0xB54B, 0x8528, 0x9509, 
            0xE5EE, 0xF5CF, 0xC5AC, 0xD58D, 0x3653, 0x2672, 0x1611, 0x0630, 0x76D7, 0x66F6, 0x5695, 
            0x46B4, 0xB75B, 0xA77A, 0x9719, 0x8738, 0xF7DF, 0xE7FE, 0xD79D, 0xC7BC, 0x48C4, 0x58E5, 
            0x6886, 0x78A7, 0x0840, 0x1861, 0x2802, 0x3823, 0xC9CC, 0xD9ED, 0xE98E, 0xF9AF, 0x8948, 
            0x9969, 0xA90A, 0xB92B, 0x5AF5, 0x4AD4, 0x7AB7, 0x6A96, 0x1A71, 0x0A50, 0x3A33, 0x2A12, 
            0xDBFD, 0xCBDC, 0xFBBF, 0xEB9E, 0x9B79, 0x8B58, 0xBB3B, 0xAB1A, 0x6CA6, 0x7C87, 0x4CE4, 
            0x5CC5, 0x2C22, 0x3C03, 0x0C60, 0x1C41, 0xEDAE, 0xFD8F, 0xCDEC, 0xDDCD, 0xAD2A, 0xBD0B, 
            0x8D68, 0x9D49, 0x7E97, 0x6EB6, 0x5ED5, 0x4EF4, 0x3E13, 0x2E32, 0x1E51, 0x0E70, 0xFF9F, 
            0xEFBE, 0xDFDD, 0xCFFC, 0xBF1B, 0xAF3A, 0x9F59, 0x8F78, 0x9188, 0x81A9, 0xB1CA, 0xA1EB, 
            0xD10C, 0xC12D, 0xF14E, 0xE16F, 0x1080, 0x00A1, 0x30C2, 0x20E3, 0x5004, 0x4025, 0x7046, 
            0x6067, 0x83B9, 0x9398, 0xA3FB, 0xB3DA, 0xC33D, 0xD31C, 0xE37F, 0xF35E, 0x02B1, 0x1290, 
            0x22F3, 0x32D2, 0x4235, 0x5214, 0x6277, 0x7256, 0xB5EA, 0xA5CB, 0x95A8, 0x8589, 0xF56E, 
            0xE54F, 0xD52C, 0xC50D, 0x34E2, 0x24C3, 0x14A0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405, 
            0xA7DB, 0xB7FA, 0x8799, 0x97B8, 0xE75F, 0xF77E, 0xC71D, 0xD73C, 0x26D3, 0x36F2, 0x0691, 
            0x16B0, 0x6657, 0x7676, 0x4615, 0x5634, 0xD94C, 0xC96D, 0xF90E, 0xE92F, 0x99C8, 0x89E9, 
            0xB98A, 0xA9AB, 0x5844, 0x4865, 0x7806, 0x6827, 0x18C0, 0x08E1, 0x3882, 0x28A3, 0xCB7D, 
            0xDB5C, 0xEB3F, 0xFB1E, 0x8BF9, 0x9BD8, 0xABBB, 0xBB9A, 0x4A75, 0x5A54, 0x6A37, 0x7A16, 
            0x0AF1, 0x1AD0, 0x2AB3, 0x3A92, 0xFD2E, 0xED0F, 0xDD6C, 0xCD4D, 0xBDAA, 0xAD8B, 0x9DE8, 
            0x8DC9, 0x7C26, 0x6C07, 0x5C64, 0x4C45, 0x3CA2, 0x2C83, 0x1CE0, 0x0CC1, 0xEF1F, 0xFF3E, 
            0xCF5D, 0xDF7C, 0xAF9B, 0xBFBA, 0x8FD9, 0x9FF8, 0x6E17, 0x7E36, 0x4E55, 0x5E74, 0x2E93, 
            0x3EB2, 0x0ED1, 0x1EF0 )
    
    accum = 0xFFFF
    
    for c in data:
            accum = (((accum << 8) & 0xFFFF) ^ ccitt_16[(accum >> 8) ^ ord(c)]) & 0xFFFF
    
    return accum

def ParseSerial(s):
    if s == "":
        return 0
    if not s.isdigit():
        return "Serial must contain only numbers and dashes"
    n = int(s)
    if not (0 < n < 0xFFFFFFFF):
        return "Serial must be between 0 and 4294967295"
    mod = n & 0xFF
    if mod == 0x00 or mod == 0xFF:
        return "Last byte of serial cannot be 0x00 or 0xFF"
    return n

MAXPORTS = 64
def scan():
        """scan for available ports. return a list of the names"""
        available = []
        for i in xrange(MAXPORTS):
            try:
                s = serial.Serial(i)
                available.append(s.portstr)
                s.close()   # explicit close 'cause of delayed GC in java
            except serial.SerialException:
                pass
        return available


print "Validation Tool Device ID programmer v1.0.4"

reset_needed = False
port = None
while(True):

    if port: port.close()
    if not reset_needed:
        print ""
        i = raw_input("Plug in the next device and hit Enter ('exit' to exit) ")
        if i == 'exit': break

    available_ports = scan()
    if not available_ports:
        print "No available COM ports detected. If you've plugged a board in, wait for Windows to finish recognizing the device."
        reset_needed = False
        print ""
    else:
        try:
##            port = serial.Serial(port_name, BAUD, timeout=0.5)
            port_name = available_ports[-1]
            port = serial.Serial(port_name, BAUD, timeout=0.5)
        except serial.SerialException as e:
           print e
           port_name = raw_input("COM port? ")
           port = serial.Serial(port_name, BAUD, timeout=0.5)
        print "Using port "+port_name
        print ""
        if not reset_needed:
            i = raw_input("Enter device ID (Enter to just retrieve): ")
            dev_id = ParseSerial(i)
        else:
            dev_id = 0
        reset_needed = False
        
        if type(dev_id) is str:
            print dev_id
        elif type(dev_id) is int:
            if dev_id:
                print "Configuring device with id "+str(dev_id)
                port.flushInput()
                port.flushOutput()
                port.write(CreateJ3Message(OP_PHY_ADDR, ACTION_SET, pack("<I",dev_id), ptype=PTYPE_ZCON,
                                           source=DEVICE_ZCONP, target=DEVICE_ZCONPR, gps=""))
                time.sleep(1)

            print "Retrieving device ID info"
            port.flushInput()
            port.flushOutput()
            port.write(CreateJ3Message(OP_DEVICE_INFO, ACTION_GET, ptype=PTYPE_ZCON,
                                       source=DEVICE_ZCONP, target=DEVICE_ZCONPR, gps=""))
            
            for i in xrange(10):
                msg = ReadJ3Message(port)
                print repr(msg)
                if msg:
                    op = msg[2]
                    action = msg[3]
                    if op == OP_PHY_ADDR: # and action == ACTION_SET:
                        pass
                    elif op == OP_DEVICE_INFO: # and action == ACTION_SET:
                        try:
                            returned_id = unpack("<I",msg[4][-5:-1])[0]
                        except Exception as e:
                            print "Invalid data returned from the device: "+str(e)
                        else:
                            print ""
                            print "Returned Device ID:", returned_id
                            if returned_id == 305419896: # 305419897 for truck install tool
                                raw_input("Power cycle board and check device ID again (hit enter).")
                                reset_needed = True
                            if returned_id == 0xFFFFFFFF:
                                print "Empty Device ID. Board needs to be provisioned."
                    elif op == OP_RESET and action == ACTION_RESET:
                        reset_needed = True
                    elif action == ACTION_ACK:
                        pass
                    elif action == ACTION_NO_ACK:
                        print "NACK received"
                    else:
                        print "Unknown message {0!r} {1!r}".format(op,action)
                    break
            else:
                print "No response from the board."

if port: port.close()
