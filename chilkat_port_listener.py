import sys, time
import chilkat

listenSocket = chilkat.CkSocket()

success = listenSocket.UnlockComponent("Anything for 30-day trial")
if (success != True):
    print "Failed to unlock component"
    sys.exit()

#  Bind to a port and listen for incoming connections:
#  This example will listen at port 5555 and allows for a backlog
#  of 25 pending connection requests.
success = listenSocket.BindAndListen(5555,25)
if (success != True):
    print listenSocket.lastErrorText()
    sys.exit()

#  Get the next incoming connection
#  Wait a maximum of 20 seconds (20000 millisec)

connectedSocket = listenSocket.AcceptNextConnection(5000)
if (connectedSocket == None ):
    print listenSocket.lastErrorText()
    sys.exit()

#  Set maximum timeouts for reading an writing (in millisec)
connectedSocket.put_MaxReadIdleMs(10000)
connectedSocket.put_MaxSendIdleMs(10000)

#  Send a "Hello World!" message to the client:
success = connectedSocket.SendString("Hello World!")
if (success != True):
    print connectedSocket.lastErrorText()

    sys.exit()

time.sleep(10)

#  Close the connection with the client.
#  Wait a max of 20 seconds (20000 millsec)
connectedSocket.Close(20000)
