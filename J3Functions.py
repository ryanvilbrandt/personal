'''
@title J3 Functions library
@author Ryan Vilbrandt
@date_created 2014-04-28
@copyright Zonar Systems, Inc

This module is meant to be an abstraction for any other code that needs to send
messages to or receive messages from the V3 or similar devices.
Some code will have its own functions for building a message and then sending
it and receiving a response (e.g. GetStatusInfo). Some code will need to call
the CreateMessageName function first, and send it to the device using SendZRequest.
'''

import struct, time
from serial import SerialException

DEBUG = False
if DEBUG:
    import sys
    sys.stdout = open("j3_stdout.log", "a")
    sys.stderr = open("j3_stderr.log", "a")

PACKET_VERSION  = '\x03'
NULL8           = '\x00'
NULL16          = '\x00\x00'
NULL32          = '\x00\x00\x00\x00'

# Packet types
PTYPE_SET_DEV_ID            = '\x09'
PTYPE_GET_DEV_ID            = '\x0A'
PTYPE_SET_CONF_VAL          = '\x0D'
PTYPE_FW_UPDATE_T           = '\x15'
PTYPE_GET_CONF_VAL          = '\x18'
PTYPE_GET_STATUS_INFO       = '\x1D'
PTYPE_ZCON                  = '\x34' #'4'
PTYPE_SET_DEV_ID_R          = '\x89'
PTYPE_GET_DEV_ID_R          = '\x8A'
PTYPE_SET_CONF_VAL_R        = '\x8D'
PTYPE_FW_UPDATE_R           = '\x95'
PTYPE_GET_CONF_VAL_R        = '\x98'
PTYPE_GET_STATUS_INFO_R     = '\x9D'
PTYPE_ZCON_MOBILE           = '\xB4'

# Device IDs
DEVICE_GPS              = '\x04'
DEVICE_PC               = '\x06'
DEVICE_J3               = '\x09' #\t
DEVICE_ZCONMD           = '\x0C'
DEVICE_ZCONMDR          = '\x0D' #\r
DEVICE_ZCONP            = '\x0E'
DEVICE_ZCONPR           = '\x0F'
DEVICE_ZCONT            = '\x10'
DEVICE_ZCONTR           = '\x11'
DEVICE_ZCONMDP          = '\x12'
DEVICE_V3               = '\x13'

ZCON_HEADER_VERSION = '\x01'

# ZCon Operations
OP_PUMP_DATA    = '\x00'
OP_TRAILER_ID   = '\x01'
OP_DEVICE_INFO  = '\x02'
OP_JOIN_ID      = '\x03'
OP_RESET        = '\x04'
OP_PING         = '\x05'
OP_PHY_ADDR     = '\x06'
OP_RSSI         = '\x07'
OP_TRUCK_INFO   = '\x08'
OP_NETWORK      = '\x09' #\t
OP_DEBUG        = '\x0A' #\n
OP_PROV         = '\x0B'
OP_DEBUG        = '\x0C'
OP_TRAILER_DATA = '\x0D'

# ZCon Actions
ACTION_SET      = '\x00'
ACTION_GET      = '\x01'
ACTION_ACK      = '\x02'
ACTION_RESET    = '\x03'
ACTION_NO_ACK   = '\x04'

# ZCON Prov operations
PROV_IR_DATA_SENT   = '\x00'
PROV_TRAILER_DATA   = '\x01'

# Firmware Update Stage IDs
FWID_UPDATE_STAGE_DELETE    = '\x00\x00'
FWID_UPDATE_STAGE_WRITE_FW  = '\x01\x00'
FWID_UPDATE_STAGE_COMPLETE  = '\x02\x00'
FWID_UPDATE_STAGE_REBOOT    = '\x03\x00'
FWID_UPDATE_STAGE_APP_TYPE  = '\x04\x00'

FW_STAGE_ERROR  = '\x80'

# Firmware Update Error IDs
FWID_UPDATE_ERASE_ERROR         = '\x00\x00'
FWID_UPDATE_NULL_DATA_ERROR     = '\x01\x00'
FWID_UPDATE_DATA_SIZE_ERROR     = '\x02\x00'
FWID_UPDATE_WRITE_ERROR         = '\x03\x00'
FWID_UPDATE_CS_ERROR            = '\x04\x00'
FWID_UPDATE_APP_TYPE_ERROR      = '\x05\x00'
FWID_UPDATE_WRITE_INDEX_ERROR   = '\x06\x00'

# Firmware Update App Type IDs
FWID_UPDATE_APP_UNKNOWN     = '\x00\x00'
FWID_UPDATE_APP_STANDARD    = '\x01\x00'
FWID_UPDATE_APP_BOOTLOADER  = '\x02\x00'

def SendTextToDevice(port, to_send, ret_text="", tries=1, timeout=0.5):
    '''
    @param serial.Serial port: An opened Serial instance.
    @param str to_send: The text to send through the serial port
    @param str ret_text: Optional; If set, the function will wait until the
        text coming back from the DUT has the specified string
        in it before returning. If this isn't set, tries and
        timeout are meaningless.
    @param int tries: The number of times the function will send to_send with
        no response before failing out.
    @param float timeout: Time in seconds for the port to wait for another char
        to come in through the serial port. This value rarely needs to be
        longer than 1 second.

    @return str or None: Will return an empty string if ret_text is an empty
        string.
        Will return a string if ret_text is set and a valid
        response is returned from the DUT.
        Will return None if ret_text is set but the function
        times out (see end_time) before a valid response from
        the DUT is returned.
    '''
    port.flushInput()
    port.flushOutput()
    # If we're looking for text returned, read from serial port and check returned
    # text for the pattern.
    # If not, just send and return with an empty string.
    if ret_text:
        # Set the port timeout to the specified timeout for this run
        old_timeout = port.timeout
        port.timeout = timeout
        while tries > 0:
            tries -= 1
            # Send the message once per try
            port.write(str(to_send))
            # Read all the data coming in through the serial until
            # data stops coming and the read() call times out
            response = port.readall()
            if str(ret_text) in response:
                port.timeout = old_timeout
                return response
        else:
            print "Loop timed out before getting response"
            print response
            port.timeout = old_timeout
            return None
    else:
        port.write(str(to_send))
        return ""

def PackVehicleData(zid, vin, odo, hours, fuel_used,
                    fuel_needed, def_needed, velocity, faults):
    '''
    @params -- zid and vin are str, all others are int
    Takes the vehicle data used during ZTerm transactions and packs it into a
    data string.
    @return str
    '''
    try:
        data = (str(zid)+
                str(vin)+
                struct.pack("<I", int(odo))+
                struct.pack("<I", int(hours))+
                struct.pack("<I", int(fuel_used))+
                struct.pack("<H", int(fuel_needed))+
                struct.pack("<H", int(def_needed))+
                struct.pack("<H", int(velocity))+
                struct.pack("<B", int(faults)))
    except Exception as e:
        print "Invalid data to be packed:\n{0}".format(e)
    else:
        return data

def CreateMessage(ptype, source, target, body=''):
    '''
    @param ptype -- str
    @param source -- str
    @param target -- str
    @param body -- str, already-packed payload for the message
    Creates a valid ZPacket message, using the given body data
    @return str -- Valid ZMessage or None
    '''
    # Prepend start bytes and length
    try:
        length = struct.pack("<H", 10+len(body))
    except Exception as e:
        print "Invalid packet length:\n{0}".format(e)
        return None
    out = "\x02" + PACKET_VERSION + length + ptype + source + target + body
    # Append CRC and stop byte, and return
    try:
        crc = struct.pack("<H", CalcCRC16(out))
    except Exception as e:
        print "Invalid CRC:\n{0}".format(e)
        return None
    sent = out + crc + '\x03'
    if DEBUG:
        print "Message built:", repr(sent)
    return sent

def SendZRequest(port, msg_to_send, timeout=5, tries=3,
                  my_id='', ret_packet=''):
    '''
    @param port -- serial.Serial
    @param msg_to_send -- str
    @param timeout -- int
    @param tries -- int
    @param my_id -- str, If defined, then this function will only listen for
        messages send to that device ID. e.g. PC is \x06
    @param ret_packet -- str, If defined, then this function will only listen
        for messages with that packet ID. e.g. GetStatusInfo response is \x9D
    Takes a serial port, and a ZMessage (str), sends it to the device,
    and waits for a response from the device. It will send multiple times
    based on the tries param, and wait a certain amount of time between tries
    based on the timeout param. If it doesn't get a response, it returns
    None.
    @return dict or None
    '''
    port.flushInput()
    port.flushOutput()
    while tries > 0:
        tries -= 1
        try:
            port.write(msg_to_send)
            if DEBUG:
                print "Packet sent: {0!r}".format(msg_to_send)
        except SerialException as e:
            print ("Exception when trying to"+
                   "write to serial port:\n{0}".format(e))
            return None
        t = time.clock() + timeout
        while time.clock() < t:
            temp = ReadMessage(port, my_id)
            if temp:
                # if DEBUG: print "{0!r}|{1!r}|{2!r}|{3!r}".format(
                                    # temp[0],temp[1],temp[2],temp[3]
                                    # )
                if (not ret_packet) or temp[0] == ret_packet:
                    payload = ParseZRequest(temp[0], temp[3])
                    if payload:
                        d = {'ptype': temp[0],
                             'source': temp[1],
                             'target': temp[2]
                             }
                        return dict(d.items() + payload.items())
    return None

def ParseZRequest(ptype, payload):
    '''
    @param ptype -- str
    @param payload -- str
    Takes a string representing a packet type (e.g. GetStatusInfo
    response == \x1D) and converts the payload into a dictionary of all the
    parameters
    return dict or None
    '''
    if ptype == PTYPE_ZCON:
        return {'zcon_message_version': payload[0],
                'op': payload[1],
                'action': payload[2],
                'payload': payload[3:]
                }
    elif ptype == PTYPE_ZCON_MOBILE:
        try:
            gpsid = struct.unpack('<I', payload[:4])
        except Exception:
            return None
        else:
            return {'gpsid': gpsid,
                    'zcon_message_version': payload[4],
                    'op': payload[5],
                    'action': payload[6],
                    'payload': payload[7:]
                    }
    elif ptype == PTYPE_FW_UPDATE_R:
        return {'stage_id': payload[0:2],
                'X_of': payload[2:4],
                'limit': payload[4:6],
                'error': payload[6:]
                }
    elif ptype == PTYPE_SET_DEV_ID_R:
        return {'device_id': myunpack(payload[0:4])
                }
    elif ptype == PTYPE_GET_STATUS_INFO_R:
        return {'status_mask': payload[0:4],
                'engine_hours': myunpack(payload[4:8]),
                'idle_hours': myunpack(payload[8:12]),
                'odometer': myunpack(payload[12:16]),
                'log_entry_count': myunpack(payload[16:20]),
                'device_id': myunpack(payload[20:24]),
                'battery_voltage': myunpack(payload[24:28]),
                'firmware_version': payload[28:56].strip('\x00'),
                'bootloader_version': myunpack(payload[56:58]),
                'unsent_inspection_count': myunpack(payload[58:60]),
                'board_revision': myunpack(payload[60:62]),
                # To be completed
                'modem_info': payload[96:]
                }
    else:
        if DEBUG:
            print "Unrecognized packet type when parsing payload"
        return {'payload': payload}

def myunpack(s, signed=False, LSB=True):
    '''
    Wrapper function for struct.unpack. Determines the data type to unpack to
    based on the length of the string passed in. Defaults to < and unsigned.
    '''
    align = "<" if LSB else ">"
    if len(s) == 1:
        data_type = "b"
    elif len(s) == 2:
        data_type = "h"
    elif len(s) == 4:
        data_type = "i"
    elif len(s) == 8:
        data_type = "q"
    else:
        data_type = "p"
    if not signed:
        data_type = data_type.upper()
    return struct.unpack(align+data_type, s)[0]

## reversed crc algoithm, crc must start out at 0xFFFF */
def CalcCRC16(data):
    '''
    @param data -- str
    Calculates the CRC16 for the given string
    @return int
    '''
    ccitt_16 = (
        0x0000, 0x1021, 0x2042, 0x3063, 0x4084, 0x50A5, 0x60C6, 0x70E7,
        0x8108, 0x9129, 0xA14A, 0xB16B, 0xC18C, 0xD1AD, 0xE1CE, 0xF1EF,
        0x1231, 0x0210, 0x3273, 0x2252, 0x52B5, 0x4294, 0x72F7, 0x62D6,
        0x9339, 0x8318, 0xB37B, 0xA35A, 0xD3BD, 0xC39C, 0xF3FF, 0xE3DE,
        0x2462, 0x3443, 0x0420, 0x1401, 0x64E6, 0x74C7, 0x44A4, 0x5485,
        0xA56A, 0xB54B, 0x8528, 0x9509, 0xE5EE, 0xF5CF, 0xC5AC, 0xD58D,
        0x3653, 0x2672, 0x1611, 0x0630, 0x76D7, 0x66F6, 0x5695, 0x46B4,
        0xB75B, 0xA77A, 0x9719, 0x8738, 0xF7DF, 0xE7FE, 0xD79D, 0xC7BC,
        0x48C4, 0x58E5, 0x6886, 0x78A7, 0x0840, 0x1861, 0x2802, 0x3823,
        0xC9CC, 0xD9ED, 0xE98E, 0xF9AF, 0x8948, 0x9969, 0xA90A, 0xB92B,
        0x5AF5, 0x4AD4, 0x7AB7, 0x6A96, 0x1A71, 0x0A50, 0x3A33, 0x2A12,
        0xDBFD, 0xCBDC, 0xFBBF, 0xEB9E, 0x9B79, 0x8B58, 0xBB3B, 0xAB1A,
        0x6CA6, 0x7C87, 0x4CE4, 0x5CC5, 0x2C22, 0x3C03, 0x0C60, 0x1C41,
        0xEDAE, 0xFD8F, 0xCDEC, 0xDDCD, 0xAD2A, 0xBD0B, 0x8D68, 0x9D49,
        0x7E97, 0x6EB6, 0x5ED5, 0x4EF4, 0x3E13, 0x2E32, 0x1E51, 0x0E70,
        0xFF9F, 0xEFBE, 0xDFDD, 0xCFFC, 0xBF1B, 0xAF3A, 0x9F59, 0x8F78,
        0x9188, 0x81A9, 0xB1CA, 0xA1EB, 0xD10C, 0xC12D, 0xF14E, 0xE16F,
        0x1080, 0x00A1, 0x30C2, 0x20E3, 0x5004, 0x4025, 0x7046, 0x6067,
        0x83B9, 0x9398, 0xA3FB, 0xB3DA, 0xC33D, 0xD31C, 0xE37F, 0xF35E,
        0x02B1, 0x1290, 0x22F3, 0x32D2, 0x4235, 0x5214, 0x6277, 0x7256,
        0xB5EA, 0xA5CB, 0x95A8, 0x8589, 0xF56E, 0xE54F, 0xD52C, 0xC50D,
        0x34E2, 0x24C3, 0x14A0, 0x0481, 0x7466, 0x6447, 0x5424, 0x4405,
        0xA7DB, 0xB7FA, 0x8799, 0x97B8, 0xE75F, 0xF77E, 0xC71D, 0xD73C,
        0x26D3, 0x36F2, 0x0691, 0x16B0, 0x6657, 0x7676, 0x4615, 0x5634,
        0xD94C, 0xC96D, 0xF90E, 0xE92F, 0x99C8, 0x89E9, 0xB98A, 0xA9AB,
        0x5844, 0x4865, 0x7806, 0x6827, 0x18C0, 0x08E1, 0x3882, 0x28A3,
        0xCB7D, 0xDB5C, 0xEB3F, 0xFB1E, 0x8BF9, 0x9BD8, 0xABBB, 0xBB9A,
        0x4A75, 0x5A54, 0x6A37, 0x7A16, 0x0AF1, 0x1AD0, 0x2AB3, 0x3A92,
        0xFD2E, 0xED0F, 0xDD6C, 0xCD4D, 0xBDAA, 0xAD8B, 0x9DE8, 0x8DC9,
        0x7C26, 0x6C07, 0x5C64, 0x4C45, 0x3CA2, 0x2C83, 0x1CE0, 0x0CC1,
        0xEF1F, 0xFF3E, 0xCF5D, 0xDF7C, 0xAF9B, 0xBFBA, 0x8FD9, 0x9FF8,
        0x6E17, 0x7E36, 0x4E55, 0x5E74, 0x2E93, 0x3EB2, 0x0ED1, 0x1EF0
        )

    accum = 0xFFFF

    for c in data:
        accum = (((accum << 8) & 0xFFFF) ^ ccitt_16[(accum >> 8) ^ ord(c)]) & 0xFFFF

    return accum

def ReadJ3Message(port, my_id='', tries=5):
    '''
    (DEPRECATED Use SendZRequest)
    Separates out the gps id, op, and action from the rest of the payload of a
    J3 message
    '''
    for i in xrange(tries):
        temp = ReadMessage(port, my_id)
        if temp:
            break
    if not temp:
        return temp
    if temp[0] == PTYPE_ZCON:
        igps = 0
    elif temp[0] == PTYPE_ZCON_MOBILE:
        igps = 4
    if DEBUG:
        print "Pieces: {0!r}|{1!r}|{2!r}|{3!r}|{4!r}".format(
                temp[1], temp[2], temp[3][1+igps], temp[3][2+igps],
                temp[3][3+igps:]
                )
    return (temp[1],            # source
            temp[2],            # target
            temp[3][1+igps],    # op
            temp[3][2+igps],    # action
            temp[3][3+igps:],   # payload
            temp[3][:igps])     # gpsid

def ReadFwUpdateMessage(port, my_id=''):
    '''
    (DEPRECATED Use SendZRequest)
    Separates out the stage_id, X_of, limit, and error from a FW update
    message
    '''
    temp = ReadMessage(port, my_id)
    if not temp:
        return temp
    ptype = temp[0]
    source = temp[1]
    target = temp[2]
    stage_id = temp[3][0:2]
    X_of = temp[3][2:4]
    limit = temp[3][4:6]
    error = temp[3][6:]
    if DEBUG:
        print "{0!r}|{1!r}|{2!r}|{3!r}|{4!r}|{5!r}|{6!r}".format(
                ptype, source, target, stage_id, X_of, limit, error
                )
    return (ptype, source, target, stage_id, X_of, limit, error)

def ReadMessage(port, my_id=''):
    '''
    @param port -- serial.Serial
    @param my_id -- str, If defined, then this function will only listen for
        messages send to that device ID. e.g. PC is \x06
    Retrieves data off the serial line. If the data is a valid ZMessage, then
    check the CRC and break up the message into ptype, source, target, and
    payload.
    @return 4-tuple (ptype, source, target, payload)
    '''
    try:
        # Read next character from the serial port
        line = port.read(1)
    except SerialException as e:
        # If something stupid happens, fail gracefully
        line = ""

    if DEBUG:
        print repr(line)
    # If the next two characters are '\x02\x03', we have a valid message
    if line == '\x02' and port.read(1) == PACKET_VERSION:
        # Grab the length bytes and read out the rest of the message
        packet = '\x02' + PACKET_VERSION + port.read(2)
        if DEBUG:
            print "Packet header received: {0!r}".format(packet)

        try:
            length = struct.unpack("<H", packet[2:4])[0]
        except Exception as e:
            print "Error when unpacking packet length:\n{0}".format(e)
            return None
        packet += port.read(length-4)
        if DEBUG:
            print "Packet received: {0!r}".format(packet)

        try:
            packet_crc = struct.unpack("<H", packet[-3:-1])[0]
        except Exception as e:
            print "Invalid CRC value in packet:\n{0}".format(e)
            return None
        # If the CRC is incorrect, ignore this packet
        if packet_crc == CalcCRC16(packet[:-3]):
            ptype = packet[4]
            # Get source and target
            source = packet[5]
            target = packet[6]
            payload = packet[7:-3]
            # Only return the message if it was meant for me
            if (not my_id) or my_id == target:
                return (ptype, source, target, payload)
        elif DEBUG:
            print "Bad CRC:", repr(packet)

    return None

def CreateJ3Message(op, action, payload="", ptype=PTYPE_ZCON_MOBILE,
                    source=DEVICE_J3, target=DEVICE_ZCONP, gps=0x00):
    '''
    Creates message for sending ZCon data.
    @return str -- Valid ZMessage
    '''
    try:
        gps = struct.pack("<I", gps)
    except Exception:
        gps = '\x00\x00\x00\x00'
    # Prepend header
    if op == OP_PUMP_DATA:
        vers = '\x02'
    else:
        vers = ZCON_HEADER_VERSION
    if ptype == PTYPE_ZCON_MOBILE:
        body = gps + vers + op + action + payload
    elif ptype == PTYPE_ZCON:
        body = vers + op + action + payload
    else:
        return None
    return CreateMessage(ptype, source, target, body)

def CreateSetDevIdMessage(gpsid, ptype=PTYPE_SET_DEV_ID,
                          source=DEVICE_PC, target=DEVICE_V3):
    '''
    Creates message for requesting status info from the V3.
    @return str -- Valid ZMessage
    '''
    body = struct.pack("<I", gpsid)
    return CreateMessage(ptype, source, target, body)

def CreateStatusInfoMessage(ptype=PTYPE_GET_STATUS_INFO,
                            source=DEVICE_PC, target=DEVICE_V3):
    '''
    Creates message for requesting status info from the V3.
    @return str -- Valid ZMessage
    '''
    return CreateMessage(ptype, source, target)

def CreateGetConfValMessage(conf,
                            ptype=PTYPE_GET_CONF_VAL,
                            source=DEVICE_PC, target=DEVICE_V3):
    '''Creates message for retrieving a conf value.'''
    return CreateMessage(ptype, source, target)

def CreateSetConfValMessage(conf, val,
                            ptype=PTYPE_SET_CONF_VAL,
                            source=DEVICE_PC, target=DEVICE_V3):
    '''
    @param int conf: The parameter address
    @param str val: The value to be assigned to the parameter
    @param str ptype: The packet type, represented as an ASCII character
    @param str source: The device ID of the source device, as an ASCII character
    @param str target: The device ID of the target device, as an ASCII character

    Creates message for setting a conf value.

    @return str -- Valid ZMessage
    '''
    body = struct.pack("<H", conf) + str(val)
    return CreateMessage(ptype, source, target, body)

def CreateFwUpdateMessage(stage, x_of=NULL16, limit=NULL16, payload="",
                          ptype=PTYPE_FW_UPDATE_T, source=DEVICE_PC,
                          target=DEVICE_V3):
    '''
    Creates message for sending a firmware update.
    @return str -- Valid ZMessage
    '''
    body = stage + x_of + limit + payload
    return CreateMessage(ptype, source, target, body)

def SendFwRebootMessage(port, tries=3, timeout=4):
    msg = CreateFwUpdateMessage(FWID_UPDATE_STAGE_REBOOT)
    return SendZRequest(port, msg, ret_packet=PTYPE_FW_UPDATE_R, tries=tries, timeout=timeout)

def SendFwAppTypeMessage(port, app_type, tries=3, timeout=4):
    msg = CreateFwUpdateMessage(FWID_UPDATE_STAGE_APP_TYPE, payload=app_type)
    return SendZRequest(port, msg, ret_packet=PTYPE_FW_UPDATE_R, tries=tries, timeout=timeout)

def SendFwDeleteMessage(port, tries=3, timeout=4):
    msg = CreateFwUpdateMessage(FWID_UPDATE_STAGE_DELETE)
    return SendZRequest(port, msg, ret_packet=PTYPE_FW_UPDATE_R, tries=tries, timeout=timeout)

def SendFwWriteMessage(port, chunk_count, max_chunks, app_chunk, tries=1, timeout=4):
    msg = CreateFwUpdateMessage(FWID_UPDATE_STAGE_WRITE_FW, chunk_count, max_chunks, app_chunk)
    return SendZRequest(port, msg, ret_packet=PTYPE_FW_UPDATE_R, tries=tries, timeout=timeout)

def SendFwFinalizeMessage(port, tries=3, timeout=4):
    msg = CreateFwUpdateMessage(FWID_UPDATE_STAGE_COMPLETE)
    return SendZRequest(port, msg, ret_packet=PTYPE_FW_UPDATE_R, tries=tries, timeout=timeout)

def GetStatusInfo(port, tries=4, timeout=5):
    '''
    Gets the status info of the attached V3
    @return str -- Response from device or None
    '''
    return SendZRequest(port, CreateStatusInfoMessage(),
                        ret_packet=PTYPE_GET_STATUS_INFO_R,
                        tries=tries, timeout=timeout)

def SetGpsid(port, gpsid, tries=3, timeout=5):
    '''
    Sets the GPSID of the unit
    @return str -- Response from device or None
    '''
    return SendZRequest(port, CreateSetDevIdMessage(gpsid),
                        ret_packet=PTYPE_SET_DEV_ID_R,
                        tries=tries, timeout=timeout)

def GetConfVal(port, conf, tries=3, timeout=5):
    return SendZRequest(port, CreateGetConfValMessage(conf),
                        ret_packet=PTYPE_GET_CONF_VAL_R,
                        tries=tries, timeout=timeout)

def SetConfVal(port, conf, val, tries=3, timeout=5):
    '''
    @param Serial port: The port to do communication over.
        Should be a valid pySerial Serial object.
    @param int conf: The parameter address
    @param str val: The value to be assigned to the parameter
    @param int tries: The number of times the message will be written
        to the serial port.
    @param int timeout: The timeout (in seconds) after a message is written
        while the app waits for a response from the V3

    Sets a conf value on the attached V3

    @return str -- Response from device or None
    '''
    return SendZRequest(port, CreateSetConfValMessage(conf, str(val)),
                        ret_packet=PTYPE_SET_CONF_VAL_R,
                        tries=tries, timeout=timeout
                        )

def PowerReset(port):
    '''Sets the param 8089 to "1", triggering a soft reset'''
    response = SetConfVal(port, 8089, "1")
    if response is None:
        return "No response when setting Power Reset conf val"

def TriggerFormatNAND(port, gpsid):
    '''Sets the param 41 to <gpsid>, triggering a low level NAND format'''
    if SetConfVal(port, 41, str(gpsid)) is None:
        return "No response when setting Trigger NAND Format conf val"

def ShellFormatNAND(port, gpsid):
    '''
    Send shell command "nand format" and wait for response.
    DO NOT USE. TriggerFormatNAND instead.
    '''
    raise NotImplementedError
