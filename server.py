 #!/usr/bin/env python
import socket
def socketListen():
    try:
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 6627)) #bound to 127.0.0.1 and port 7070
        s.listen(1) #At this point only listening for one connection
        clientConn, addrinfo=s.accept()
        return clientConn
    except Exception, e:
        print e
def main():
    clientConn=socketListen()
    print "Listening..."
    try:
        for i in xrange(100):
            MSG=clientConn.recv(1024)
            print "MSG:",repr(MSG)
            print dir(clientConn)
        clientConn.close()
        print "Connection closedexiting"
    except KeyboardInterrupt:
        print "KeyboardInterrupt"
        try:
            clienConn.close()
        except:
            print "Failed to close connection."
    except Exception, e:
        print e
        try:
            clienConn.close()
        except:
            pass
if __name__ == "__main__": main() 
