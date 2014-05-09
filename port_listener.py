import socket, time, threading, select, serial, sys, os, struct

class Main(object):
        ListenThreadRunning = False
        RunThreads = True
        port = 8123
        f = None

        def __init__(self):

##                self.f = open('listener log.txt','w')
                
                t = threading.Thread(name="ListenerThread", target=self.PortListen)
                t.start()

                print "Running, press Ctrl+C to break"
                try:
                    while(self.RunThreads):
                        pass
                except KeyboardInterrupt:
                    print ""
                    print "Exitting..."

                self.RunThreads = False
                
                while self.ListenThreadRunning: pass

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

        def PortListen(self):
            self.ListenThreadRunning = True
            s = None
            while not s:
                if not self.RunThreads:
                    ListenThreadRunning = False
                    return
                s = self.socketBind(port=self.port)
            print "Listening to messages on port {0}...".format(self.port)
            clientConn = None
            while self.RunThreads:
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
                    if clientConn:
                        try:
                            ready = select.select([clientConn], [], [], 0)
                            if ready[0]:
                                MSG = clientConn.recv(1024)
                        except Exception, e:
                            print "{0!r}".format(e)
                            print "Closing connection...\n"
                            if clientConn: clientConn.close()
                            clientConn = None
                        else:
                            if MSG:
                                print "RECV: {0!r}".format(MSG)
        ##                        self.f.write("[{0}] {1}\n".format(time.ctime(),repr(MSG)))
                    else:
                        time.sleep(0.5)
            try:
                clientConn.close()
                s.close()
            except:
                pass
            print "Not listening to Datalog messages anymore..."
            self.ListenThreadRunning = False
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
