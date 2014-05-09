import serial

def RequestData(comPort):
        comPort.flushInput()
        comPort.flushOutput()
        comPort.write("1\r")
        dataList = [comPort.readline() for i in range(14)]

        if not dataList:
            self.ProcessOutput("Unable to talk to pump board. Make sure the cable is plugged in " +
                              "and the board is in provisioning mode.", "No Response From Pump Board",
                              ERROR, sound="error sound")
            return None

        try:
            n = dataList.index("Current settings:\t\n")
        except:
            self.ProcessOutput("Data returned after request for settings is unparseable. " +
                              "Please try again.", "Bad Settings Returned",
                              ERROR, sound="error sound")
            return None
        else:
            dataList = dataList[n+1:]
            for i in range(len(dataList)):
                temp = dataList[i]
                dataList[i] = temp[temp.find(": ")+2:temp.rfind("\t")]
            return dataList[:6] + dataList[6].split(':') + dataList[7:]

s = serial.Serial("COM8")

settings = '15:10.0.0.200:64.14.140.29:10.0.0.210:10.129.8.70:255.255.255.0:10.0.0.1:7879:9829:6627:64FC8C:100001:130:2\r'
s.write(settings)
print repr(settings)

print RequestData(s)

s.close()
