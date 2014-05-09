import socket
from time import sleep
serverHost = '10.0.2.210'
serverPort = 7879

print "IP address of pump board: (1 for " + serverHost + ")",
ip = raw_input()

if not (ip == "1"):
    serverHost = ip

filenames = ["ZCon0-5.bin", "ZConLED.bin"]

print("Filename on TFTP server:")
for i in range(len(filenames)):
    print str(i+1) + ") " + filenames[i]
print ("Or type in other filename")

filename = raw_input()
try:
    filename = filenames[int(filename)-1]
except:
    pass

print("")
print("IP of pump board: " + serverHost)
print("Filename: " + filename)
print("")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # create a TCP socket

try:
    s.connect((serverHost, serverPort)) # connect to server on the port
except Exception as e:
    print("Problem connecting to pump board:\n" + str(e))
else:
    print("Connection established! \\m/ >_< \\m/")


    ##filename = "ZconLED.bin"
    BOOTLOADERc = 5  ## Activating the bootloader is command 5 for the pump board

    ## Length of filename+1, command number (5), filename
    ## First two must be converted to chars
    sendString = "{}{}{}".format(chr(len(filename)+1),chr(BOOTLOADERc),filename)

    s.send(sendString)
    print("Sent string: " + repr(sendString))

    sleep(1)

    print("Closing port...")
    s.close()

    print("Done!")

print("")
raw_input("Press ENTER to continue...")
