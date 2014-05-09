import socket, time, threading, select, serial, sys, os, struct

BOOTLOADERc = 5  ## Activating the bootloader is command 5 for the pump board

class Main(object):
        DatalogThreadRunning = False
        RunThreads = True
        serverHost = '10.0.2.3'
        port = 9829
        cmd = ""
        index = 0
        f = None
##        filenames = ["ZCONP-1.0.10_08-18-2011.bin"]
##        filenames = ["ZCONP-1.0.11_08-22-2011.bin"]
##        filenames = ["ZCONP-1.0.13_08-23-2011.bin"]
##        filenames = ["ZCONP-1.0.19_09-14-2011.bin"]
##        filenames = ["ZCONP-1.0.21_09-20-2011.bin"]
##        filenames = ["ZCONP-1.0.34_12-09-2011.bin"]
        filenames = ["ZCONPR-1.0.29_12-09-2011"]

        def __init__(self):
                replies = ['$ARM FW(ZCONP-0.0.1 07/22/2011 OTA-1) ARM BL(255) Radio FW(ZCONPR-0.0.3 07/21/2011-3) Radio BL(4)\r\n',
                           '$ARM FW(ZCONP-0.0.1 07/22/2011 OTA-1) ARM BL(255) Radio FW(ZCONPR-0.0.3 07/21/2011-3) Radio BL(4)\r\n',
                           '$ARM FW(ZCONP-0.0.1 07/22/2011 OTA-2) ARM BL(255) Radio FW(ZCONPR-0.0.3 07/21/2011-3) Radio BL(4)\r\n',
                           '$ARM FW(ZCONP-0.0.1 07/22/2011 OTA-3) ARM BL(255) Radio FW(ZCONPR-0.0.3 07/21/2011-3) Radio BL(4)\r\n',
                           '$ARM FW(ZCONP-0.0.1 07/22/2011 OTA-4) ARM BL(255) Radio FW(ZCONPR-0.0.3 07/21/2011-3) Radio BL(4)\r\n',
                           '$ARM FW(ZCONP-0.0.1 07/22/2011 OTA-Def) ARM BL(255) Radio FW(ZCONPR-0.0.3 07/21/2011-3) Radio BL(4)\r\n',
                           '$ARM FW(ZCONP-0.0.1 07/22/2011 OTA-Def) ARM BL(78) Radio FW(ZCONPR-0.0.3 07/21/2011-3) Radio BL(4)\r\n',
                           '$ARM FW(ZCONP-0.0.1 07/22/2011 OTA-Def) ARM BL(255) Radio FW(ZCONPR-0.0.3 07/21/2011-3) Radio BL(4)\r\n',
                           '$ARM FW(ZCONP-0.0.1 07/22/2011 OTA-Def) ARM BL(255) Radio FW(ZCONPR-0.0.2 07/21/2011-2) Radio BL(4)\r\n',
                           '$ARM FW(ZCONP-0.0.1 07/22/2011 OTA-Def) ARM BL(255) Radio FW(ZCONPR-0.0.3 07/21/2011-3) Radio BL(4)\r\n']

                self.cmd = chr(len(self.filenames[self.index])+2) + chr(BOOTLOADERc) + self.filenames[self.index] + chr(0)

##                self.f = open("bootloader test log.txt", 'a')
                last_cmd_time = time.clock()
                
                t = threading.Thread(name="DatalogThread", target=self.DatalogListen)
                t.start()

##                PORT = 17
##                BAUD = 9600
##                REPR, Hex, HEX, oldhex = 0, 1, 2, 3
##                MODE = REPR
##
##                try:
##                   s = serial.Serial("COM{0}".format(PORT), BAUD, timeout=0.5)
##                except serial.SerialException as e:
##                   print e
##                   PORT = raw_input("COM port? ")
##                   s = serial.Serial("COM{0}".format(PORT), BAUD, timeout=0.5)

                print "Running, press Ctrl+C to break"
                newline = False
                try:
                    while(self.RunThreads):
                        pass
##                        string = s.readline()
##                        if string:
##                                print time.ctime()
##                                print "{0!r}".format(string)
##                                if string.startswith('$'):
##                                        self.f.write("[{0}] {1!r}\n".format(time.ctime(),string))
##                                        if not string == replies[self.index]:
##                                                t = "\n>>> RETURNED STRING DOES NOT MATCH EXPECTED STRING\n>>> "+replies[self.index]
##                                                print t
##                                                self.f.write("[{0}] {1!r}\n".format(time.ctime(),t))
####                                        index = (index+1) % len(self.filenames)
####                                        self.cmd = chr(len(self.filenames[index])+2) + chr(BOOTLOADERc) + self.filenames[index] + chr(0)
##                                        last_cmd_time = time.clock()
##                        # If it's been 10 minutes since the last command was sent and no response, send command again
##                        if time.clock() > last_cmd_time+600:
##                                self.cmd = chr(len(self.filenames[self.index])+2) + chr(BOOTLOADERc) + self.filenames[self.index] + chr(0)
                except KeyboardInterrupt:
                    print ""
                    print "Exitting..."
##                    s.write(' ')

##                s.close()
                self.RunThreads = False
                
                while self.DatalogThreadRunning:
                        pass

##                self.f.flush()
##                os.fsync(self.f)
##                self.f.close()

        def socketBind(self, port, timeout=None):
                try:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        if timeout:
                            s.settimeout(timeout)
                        s.bind(('', port)) #bound to localhost
                        return s
                except Exception, e:
                        print e
                        if str(e).startswith('[Errno 10048]'):
                                self.RunThreads = False
                        return None

        def DatalogListen(self):
            self.DatalogThreadRunning = True
            s = None
            while not s:
                if not self.RunThreads:
                    self.DatalogThreadRunning = False
                    print "Exitting Listen thread"
                    return
                s = self.socketBind(port=self.port)
            print "Listening to Datalog messages on port {0}...".format(self.port)
            clientConn = None
            while self.RunThreads and self.cmd:
##            while self.cmd:
                    MSG = ""
                    if not clientConn:
                        print "Attempting connection... "
                        s.listen(1) #Listen for 1 connection
                        try:
                            clientConn, a = s.accept()
                            print "Connection made!"
                        except Exception, e:
                            print "ERROR {0!r}\n".format(e)
                            if str(e).startswith('[Errno 10048]'):
                                    self.RunThreads = False
                    if clientConn and self.cmd:
                        try:
                            ready = select.select([clientConn], [], [], 0)
                            if ready[0]:
                                MSG = clientConn.recv(1024)
                        except Exception, e:
                            print "{0!r}".format(e)
                            print "Closing Datalog connection...\n"
                            if clientConn: clientConn.close()
                            clientConn = None
                        else:
                            if MSG:
                                print "RECV: {0!r}".format(MSG)
                                versions = "Pump: {0}  PR: {1}  PRBL: {2}".format(".".join([str(self.myunpack(MSG[i:i+2])) for i in xrange(147,155,2)]),
                                                                                  ".".join([str(self.myunpack(MSG[i])) for i in xrange(160,163)]),
                                                                                  self.myunpack(MSG[164:166]))
                                print "Versions:",versions
                                if self.cmd:
##                                    self.f.write("[{0}] Versions: {1}\n".format(time.ctime(),versions))
                                    string = "SEND: {0!r}".format(self.cmd)
##                                    self.f.write("[{0}] {1!r}\n".format(time.ctime(),string))
                                    print string
                                    clientConn.send(self.cmd)
                                    clientConn.close()
                                    clientConn = None
                                    self.cmd = None
##                                    self.index = (self.index+1) % len(self.filenames)
##                                    self.cmd = chr(len(self.filenames[self.index])+2) + chr(BOOTLOADERc) + self.filenames[self.index] + chr(0)
                                else:
                                    self.RunThreads = False
                    else:
                        time.sleep(0.5)
            try:
                clientConn.close()
                s.close()
            except:
                pass
            print "Not listening to Datalog messages anymore..."
            self.DatalogThreadRunning = False
            self.RunThreads = False

        def myunpack(self, data, signed=False, LSB=True, fmt=""):
                if not data:
                    return ""
                if not fmt:
                    # Get the required format of the data, based on the data length
                    d = {1:'B', 2:'H', 4:'I', 8:'Q'}
                    fmt = d.get(len(data),'B')
                    # If signed, convert fmt string to lowercase
                    if signed: fmt = fmt.lower()
                    # Determine endianness. If the LSB comes first, it's big-endian
                    if LSB: fmt="<"+fmt
                    else: fmt=">"+fmt
                return struct.unpack(fmt, data)[0]




Main()
