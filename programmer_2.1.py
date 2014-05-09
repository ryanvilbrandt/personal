from Tkinter import *
import tkMessageBox
import tkFileDialog

VERSION = "2.1"
LAST_UPDATED = "Jul 09, 2008"
FULLSCALEV = 22.26
PODI_M = 25.75569124
PODI_B = 22.48147858
current_file = ""

class Body:

    global FULLSCALEV
    
    values = []     # Actual Hex values to be written to file
    entries = []    # Values seen by the user in the Entry boxes
    master = None
    textBox = None
    scroll = None
    file_checksum = hex(0)

    def __init__(self, master):

        for i in range(25):     # Build up values list with empty strings
            self.values.append("")
        
        self.master = master
        
        frame1 = Frame(master, padx=10, pady=10)
        
        Label(frame1, text="Pod version").grid(row=00, sticky=W)
        Label(frame1, text="Pod type").grid(row=10, sticky=W)
        Label(frame1, text="Max Drive Voltage-Min Mode (Volts)").grid(row=20, sticky=W)
        Label(frame1, text="Max Drive Voltage-Max Mode (Volts)").grid(row=30, sticky=W)
        Label(frame1, text="Initial Drive Voltage-Min Mode (Volts)").grid(row=40, sticky=W)
        Label(frame1, text="Initial Drive Voltage-Max Mode (Volts)").grid(row=50, sticky=W)
        Label(frame1, text="Highest Pod Speed Setting-Min Mode (kRPM)").grid(row=60, sticky=W)
        Label(frame1, text="Highest Pod Speed Setting-Max Mode (kRPM)").grid(row=70, sticky=W)
        Label(frame1, text="Fullscale KRPM-Min Mode (kRPM)").grid(row=80, sticky=W)
        Label(frame1, text="Fullscale KRPM-Max Mode (kRPM)").grid(row=90, sticky=W)
        Label(frame1, text="Fullscale voltage (Volts)").grid(row=100, sticky=W)
        Label(frame1, text="Pod Current Limit-Min Mode (Amps)").grid(row=110, sticky=W)
        Label(frame1, text="Pod Current Limit-Max Mode (Amps)").grid(row=120, sticky=W)

        self.podVersion = Entry(frame1, name="_Pod version", width=22)
        self.podTypeVar = StringVar(frame1,"Allow Max Mode")
        self.podType = OptionMenu(frame1, self.podTypeVar, "Allow Max Mode", "Disable Max Mode")
        self.minMaxV = Entry(frame1, name="_Max Drive Voltage-Min Mode", width=22)
        self.maxMaxV = Entry(frame1, name="_Max Drive Voltage-Max Mode", width=22)
        self.minInitV = Entry(frame1, name="_Initial Drive Voltage-Min Mode", width=22)
        self.maxInitV = Entry(frame1, name="_Initial Drive Voltage-Max Mode", width=22)
        self.minMaxKRPM = Entry(frame1, name="_Highest Pod Speed Setting-Min Mode", width=22)
        self.maxMaxKRPM = Entry(frame1, name="_Highest Pod Speed Setting-Max Mode", width=22)
        self.minFullscale = StringVar(value="Calculated value")
        self.maxFullscale = StringVar(value="Calculated value")
        self.minIlim = Entry(frame1, name="_Pod Current Limit-Min Mode", width=22)
        self.maxIlim = Entry(frame1, name="_Pod Current Limit-Max Mode", width=22)

        self.podVersion.grid(row=00, column=10)
        self.podType.grid(row=10, column=10)
        self.minMaxV.grid(row=20, column=10)
        self.maxMaxV.grid(row=30, column=10)
        self.minInitV.grid(row=40, column=10)
        self.maxInitV.grid(row=50, column=10)
        self.minMaxKRPM.grid(row=60, column=10)
        self.maxMaxKRPM.grid(row=70, column=10)
        Label(frame1, textvariable=self.minFullscale).grid(row=80, column=10, sticky=W)
        Label(frame1, textvariable=self.maxFullscale).grid(row=90, column=10, sticky=W)
        Label(frame1, text=(str(FULLSCALEV) + " (Static value)")).grid(row=100, column=10, sticky=W)
        self.minIlim.grid(row=110, column=10)
        self.maxIlim.grid(row=120, column=10)

        self.entries.append(self.podVersion)
        self.entries.append(self.podTypeVar)
        self.entries.append(self.minMaxV)
        self.entries.append(self.maxMaxV)
        self.entries.append(self.minInitV)
        self.entries.append(self.maxInitV)
        self.entries.append(self.minMaxKRPM)
        self.entries.append(self.maxMaxKRPM)
        self.entries.append(Entry(frame1, name="dummy1", textvariable=StringVar(value="dummy1")))
        self.entries.append(Entry(frame1, name="dummy2", textvariable=StringVar(value="dummy2")))
        self.entries.append(self.minIlim)
        self.entries.append(self.maxIlim)
        
        Label(frame1, text="Infusion Pump Speed-Min Mode (RPM)").grid(row=00, column=20, sticky=W)
        Label(frame1, text="Infusion Pump Speed-Max Mode (RPM)").grid(row=10, column=20, sticky=W)
        Label(frame1, text="Aspiration Pump Speed-Min Mode (RPM)").grid(row=20, column=20, sticky=W)
        Label(frame1, text="Aspiration Pump Speed-Max Mode (RPM)").grid(row=30, column=20, sticky=W)
        Label(frame1, text="Infusion Pump Therapy Turn Off Delay (s)").grid(row=40, column=20, sticky=W)
        Label(frame1, text="Aspiration Pump Therapy Turn Off Delay (s)").grid(row=50, column=20, sticky=W)
        Label(frame1, text="Infusion Pump REx Turn Off Delay (s)").grid(row=60, column=20, sticky=W)
        Label(frame1, text="Aspiration Pump REx Turn Off Delay (s)").grid(row=70, column=20, sticky=W)
        Label(frame1, text="Prime Duration (s)").grid(row=80, column=20, sticky=W)
        Label(frame1, text="Tach Ratio").grid(row=90, column=20, sticky=W)
        Label(frame1, text="REx Set Voltage (Volts)").grid(row=100, column=20, sticky=W)
        Label(frame1, text="REx Direction").grid(row=110, column=20, sticky=W)

        self.minInfspd = Entry(frame1, name="_Infusion Pump Speed-Min Mode")
        self.maxInfspd = Entry(frame1, name="_Infusion Pump Speed-Max Mode")
        self.minAspspd = Entry(frame1, name="_Aspiration Pump Speed-Min Mode")
        self.maxAspspd = Entry(frame1, name="_Aspiration Pump Speed-Max Mode")
        self.infDelay = Entry(frame1, name="_Infusion Pump Therapy Turn Off Delay")
        self.aspDelay = Entry(frame1, name="_Aspiration Pump Therapy Turn Off Delay")
        self.infRex = Entry(frame1, name="_Infusion Pump REx Turn Off Delay")
        self.aspRex = Entry(frame1, name="_Aspiration Pump REx Turn Off Delay")
        self.primeDur = Entry(frame1, name="_Prime Duration")
        self.tach = Entry(frame1, name="_Tach Ratio")
        self.rexDrive = Entry(frame1, name="_REx Set Voltage")
        self.rexDirecVar = StringVar(frame1,"Normal")
        self.rexDirec = OptionMenu(frame1, self.rexDirecVar, "Normal", "Invert")
        
        self.minInfspd.grid(row=00, column=30)
        self.maxInfspd.grid(row=10, column=30)
        self.minAspspd.grid(row=20, column=30)
        self.maxAspspd.grid(row=30, column=30)
        self.infDelay.grid(row=40, column=30)
        self.aspDelay.grid(row=50, column=30)
        self.infRex.grid(row=60, column=30)
        self.aspRex.grid(row=70, column=30)
        self.primeDur.grid(row=80, column=30)
        self.tach.grid(row=90, column=30)
        self.rexDrive.grid(row=100, column=30)
        self.rexDirec.grid(row=110, column=30)

        self.entries.append(self.minInfspd)
        self.entries.append(self.maxInfspd)
        self.entries.append(self.minAspspd)
        self.entries.append(self.maxAspspd)
        self.entries.append(self.infDelay)
        self.entries.append(self.aspDelay)
        self.entries.append(self.infRex)
        self.entries.append(self.aspRex)
        self.entries.append(self.primeDur)
        self.entries.append(self.tach)
        self.entries.append(Entry(frame1, name="dummy3", textvariable=StringVar(value="dummy3")))
        self.entries.append(self.rexDrive)
        self.entries.append(self.rexDirecVar)

        Label(frame1, text=":1").grid(row=90, column=35, sticky=W)
        
        frame2 = Frame(master, padx=10, pady=10)

        Button(frame2, text="Import values...", justify=LEFT, padx=2, command=self.import_file).grid(row=00, column=00)
        Button(frame2, text="Save to file...", justify=LEFT, padx=2, command=self.save).grid(row=00, column=10)
        Button(frame2, text="Save as...", justify=LEFT, padx=2, command=self.save_as).grid(row=00, column=20)
        Button(frame2, text="Clear", justify=LEFT, padx=2, command=self.clear_values).grid(row=00, column=30)
        Button(frame2, text="Check values", justify=LEFT, padx=2, command=self.check_vals).grid(row=00, column=40)
        Button(frame2, text="Debug", justify=LEFT, padx=2, command=self.debug).grid(row=00, column=50)

        frame3 = Frame(master, padx=10, pady=10)
        
        self.textBox = Text(frame3, height=10)
        self.scroll = Scrollbar(frame3, command = self.textBox.yview)
        self.textBox.config(yscrollcommand=self.scroll.set)
        self.textBox.grid(row=00,column=00,sticky=NS)
        self.scroll.grid(row=00,column=10,sticky=NS)

        frame1.pack()
        frame2.pack()
        frame3.pack()
        
        self.appendtext("Begin the programming process by either importing a HEX file, or typing in your own values.\nWhen you're done, either Save to file... or Save as...\n - Save to file... will save to the current file you have open. \n - Save as... will allow you to save to an alternate file.")

        master.bind("<Control-s>", self.save)


    def appendtext(self, text):
        self.textBox.insert(END,text)
        self.textBox.yview_moveto(1)

    # r is the decimal place; 0 => 10, 2 => 10.27
    # Input: num=int, float, or string; r=int
    # Output: string
    def myRound(self, num, r=0):
        if type(num) is str:
            num = float(num)
        num += 0.5/(10**r)
        if r == 0:
            return str(int(num))
        else:
            num = str(num)
            return num[:num.find('.')+r+1]
    
    def debug(self):
        print str(self)[:100]
##        self.clear_values()
##        self.entries[0].insert(END, "99")
##        self.entries[1].set("Allow Max Mode")
##        self.entries[2].insert(END, "19.31")
##        self.entries[3].insert(END, "19.31")
##        self.entries[4].insert(END, "19.31")
##        self.entries[5].insert(END, "19.31")
##        self.entries[6].insert(END, "74")
##        self.entries[7].insert(END, "74")
##        #self.entries[8].insert(END, "XXXXX")
##        #self.entries[9].insert(END, "XXXXX")
##        self.entries[10].insert(END, "0.500")
##        self.entries[11].insert(END, "0.750")
##        self.entries[12].insert(END, "88")
##        self.entries[13].insert(END, "88")
##        self.entries[14].insert(END, "47")
##        self.entries[15].insert(END, "47")
##        self.entries[16].insert(END, "2")
##        self.entries[17].insert(END, "2")
##        self.entries[18].insert(END, "2")
##        self.entries[19].insert(END, "2")
##        self.entries[20].insert(END, "50")
##        self.entries[21].insert(END, "1.4")
##        #self.entries[22].insert(END, "XXXXX")
##        self.entries[23].insert(END, "8.14")
##        print "---"
##        print float(self.entries[19].get())
##        print (0.6/float(self.entries[19].get())) * 2.0**16.0
##        temp = int(((0.6/float(self.entries[19].get())) * 2.0**16.0) + 0.5)
##        print temp
##        print hex(temp)
##        self.values[19] = self.myToHex(temp/0x100) # MSB
##        self.values[20] = self.myToHex(temp%0x100) # LSB

##    def crc16_check(self, s):
##        l = s.split("\n")
##        n = 0xFFFF
##        x = l[0]
##        for i in range(4,20):
##            #print x[2*i+1:2*i+3]
##            n = self.AddByteToCRC(int(x[2*i+1:2*i+3],16),n)
##        x = l[1]
##        for i in range(4,20):
##            #print x[2*i+1:2*i+3]
##            n = self.AddByteToCRC(int(x[2*i+1:2*i+3],16),n)
##        print "------"
##        print hex(n)
####        n = self.AddByteToCRC(int(x[37:41],16),n)%(2**16)
####        print hex(n)
##    
##    def checksum_check(self, s):
##        l = s.split("\n")
##        n = 0
##        x = l[0]
##        for i in range(0,20):
##            #print x[2*i+1:2*i+3]
##            n += int(x[2*i+1:2*i+3],16)
##        n = n % 256
##        print "------"
##        print n
##        print int(x[-2:],16)
##        print (n + int(x[-2:],16))%256

    def dec2bin(self, num):
        num = int(num)
        if num == 1:
            return "0"
        if num < 0:
            return str(num)
        out = ""
        while(num != 0):
            out = str(num % 2) + out
            num = num / 2
        return out

    def clear_values(self):
        self.entries[0].delete(0, END)
        self.entries[1].set("Allow Max Mode")
        for i in range(2,24):
            self.entries[i].delete(0, END)
        self.entries[24].set("Normal")
        for x in self.values:
            x = ""
            
    def check_vals(self):
        self.appendtext("\n\nChecking for valid values...")
        err_256 = []
        noerr = [True]
        try:    # Special check for Pod Version
            x = int(self.entries[0].get(),16)
        except ValueError:
            noerr[0] = False
            name = str(self.entries[0])
            err_256.append(name[name.index("._")+2:])
        else:
            if x < 0 or x > 255:
                noerr[0] = False
                name = str(self.entries[0])
                err_256.append(name[name.index("._")+2:])
        for i in range(1,len(self.entries)):
            if i not in [1,8,9,22,24]: # List entries to not be checked here
                x = self.entries[i].get()
                #print x
                if x == "" or float(x) < 0:
                    noerr[0] = False
                    name = str(self.entries[i])
                    err_256.append(name[name.index("._")+2:])
        if noerr[0]:
            noerr.append( float(self.entries[2].get()) <= FULLSCALEV and
                          float(self.entries[3].get()) <= FULLSCALEV )
            noerr.append( float(self.entries[4].get()) <= float(self.entries[2].get()) and
                          float(self.entries[5].get()) <= float(self.entries[3].get()) )
            noerr.append( 1 <= float(self.entries[6].get()) <= 255 and
                          1 <= float(self.entries[7].get()) <= 255 )
            noerr.append( 0.300 <= float(self.entries[10].get()) <= 1.150 and
                          0.300 <= float(self.entries[11].get()) <= 1.150 )
            noerr.append( int(self.entries[12].get()) <= 160 and
                          int(self.entries[13].get()) <= 160 )
            noerr.append( int(self.entries[14].get()) <= 108 and
                          int(self.entries[15].get()) <= 108 )
            noerr.append( float(self.entries[16].get()) <= 25.5 and
                          float(self.entries[17].get()) <= 25.5 and
                          float(self.entries[18].get()) <= 25.5 and
                          float(self.entries[19].get()) <= 25.5 )
            noerr.append( float(self.entries[20].get()) <= 255 )
            noerr.append( 1 <= float(self.entries[21].get()) <= 7 )
            noerr.append( float(self.entries[23].get()) <= FULLSCALEV )
        if False in noerr:
            self.appendtext("\nValue check found errors:")
            if err_256 != []:
                self.appendtext("\n - Invalid value(s) at ")
                for s in err_256:
                    self.appendtext("\n\t" + s)
            else:
                if not noerr[1]:
                    self.appendtext("\n - Max Drive Voltage cannot exceed %f volts." % (FULLSCALEV))
                if not noerr[2]:
                    self.appendtext("\n - Initial Drive Voltage cannot exceed Max Drive Voltage.")
                if not noerr[3]:
                    self.appendtext("\n - Highest Pod Speed Setting must be within range 1 to 255 amps.")
                if not noerr[4]:
                    self.appendtext("\n - Pod Current Limit must be within range 0.300 to 1.150 amps.")
                if not noerr[5]:
                    self.appendtext("\n - Infusion Pump Speed must be within range 0 to 160 RPM.")
                if not noerr[6]:
                    self.appendtext("\n - Aspiration Pump Speed must be within range 0 to 108 RPM.")
                if not noerr[7]:
                    self.appendtext("\n - All Turn Off Delays must be within range 0 to 25.5 seconds.")
                if not noerr[8]:
                    self.appendtext("\n - Prime Duration must be within range 0 to 255 seconds.")
                if not noerr[9]:
                    self.appendtext("\n - Tach Ratio must be within range 1 to 7.")
                if not noerr[10]:
                    self.appendtext("\n - REx Set Voltage cannot exceed %f volts." % (FULLSCALEV))
        else:
            self.appendtext("\nNo errors found.")
            self.parse_values()
            self.revert(recalcFromFile=False)
            return True
        return False

    def parse_values(self):
        global PODI_M, PODI_B
        # Set the calculated GUI values
        minFSK = (FULLSCALEV/float(self.minMaxV.get())) * float(self.minMaxKRPM.get())
        maxFSK = (FULLSCALEV/float(self.maxMaxV.get())) * float(self.maxMaxKRPM.get())
        self.minFullscale.set(self.myRound(minFSK))
        self.maxFullscale.set(self.myRound(maxFSK))
        # Parse values to the PROM parameters
        self.values[0] = self.entries[0].get()[:2]
        while len(self.values[0]) < 2:
            self.values[0] = "0" + self.values[0]
        if self.podTypeVar.get() == "Allow Max Mode":
            self.values[1] = "01"
        if self.podTypeVar.get() == "Disable Max Mode":
            self.values[1] = "02"
        self.values[2] = self.myToHex(self.minMaxKRPM.get())
        self.values[3] = self.myToHex(self.maxMaxKRPM.get())
        self.values[4] = self.myToHex(float(self.minInitV.get()) / float(self.minMaxV.get()) * float(self.minMaxKRPM.get()))
        self.values[5] = self.myToHex(float(self.maxInitV.get()) / float(self.maxMaxV.get()) * float(self.maxMaxKRPM.get()))
        self.values[6] = self.myToHex( int((255.0/int(self.myRound(minFSK)))*(2**12)) >> 8 )
        self.values[7] = self.myToHex( (255.0/int(self.myRound(minFSK)))*(2**12))
        self.values[8] = self.myToHex( int((255.0/int(self.myRound(maxFSK)))*(2**12)) >> 8 )
        self.values[9] = self.myToHex( (255.0/int(self.myRound(maxFSK)))*(2**12))
        for i in range(10,12):
            try:
                x = float(self.entries[i].get())
            except ValueError:
                y = ""
            else:
                y = (PODI_M / x) - PODI_B
            self.values[i] = self.myToHex(y)
        for i in range(12,16):    # 0 to 255
            self.values[i] = self.myToHex(self.entries[i].get())
        for i in range(16,20):  # 0.0 to 25.5
            self.values[i] = self.myToHex(self.entries[i].get(),ratio=(255.0/25.5))
        self.values[20] = self.myToHex(self.entries[20].get())
        temp = int(((0.6/float(self.entries[21].get())) * 2.0**16.0) + 0.5)
        self.values[21] = self.myToHex(temp/0x100) # MSB
        self.values[22] = self.myToHex(temp%0x100) # LSB
        self.values[23] = self.myToHex(self.entries[23].get(), ratio=(255.0/FULLSCALEV))
        if self.rexDirecVar.get() == "Normal":
            self.values[24] = "00"
        elif self.rexDirecVar.get() == "Invert":
            self.values[24] = "01"
        return

    def myToHex(self, string, ratio=1.0):   # Ensures that the returned string is exactly 2 characters long
        try:
            x = float(string)
        except ValueError:
            return ""
        else:
            x = hex(int(x*ratio + 0.5))[2:]
            x = x[-2:]
            while len(x) < 2:
                x = "0"+x
            return x

##    pot_table = [1.146, 1.097, 1.052, 1.011, 0.973, 0.937, 0.904, 0.874, 0.845, 0.818, 0.793,
##                 0.769, 0.747, 0.726, 0.706, 0.687, 0.669, 0.652, 0.636, 0.621, 0.606, 0.592,
##                 0.579, 0.566, 0.554, 0.543, 0.531, 0.521, 0.510, 0.500, 0.491, 0.482, 0.473,
##                 0.464, 0.456, 0.448, 0.440, 0.433, 0.426, 0.419, 0.412, 0.406, 0.400, 0.393,
##                 0.387, 0.382, 0.376, 0.371, 0.366, 0.360, 0.355, 0.351, 0.346, 0.341, 0.337,
##                 0.332, 0.328, 0.324, 0.320, 0.316, 0.312, 0.309, 0.305, 0.301]

    def __str__(self):
        # Header
        if current_file[-4:] == ".mcs":
            s = ":020000040000FA\n:10000000"
        else:
            s = ":10000000"
        # First data line
        check = 0x10
        crc16 = 0xFFFF
        for x in self.values[0:16]:
            s += x
            check += int(x,16)
            crc16 = self.AddByteToCRC(int(x,16), crc16)
            #print crc16
        file_checksum = check - 0x10
        check = ((check%256) ^ 0xffff)+1    # 2's comp
        check = hex(check)[2:]
        check = check[-2:]
        while len(check) < 2:
            check = "0"+check
        s += check
        # Second data line
        s += '\n:10001000'
        check = 0x20
        for x in self.values[16:]:
            s += x
            check += int(x,16)
            crc16 = self.AddByteToCRC(int(x,16), crc16)
        s += "0000000000"
        for i in range(5):
            crc16 = self.AddByteToCRC(0, crc16)
        # CRC16 bytes
        # print "CRC check: %f" % self.AddByteToCRC(crc16,crc16)
        crc16 = hex(crc16)[2:]
        crc16 = crc16[-4:]
        while len(crc16) < 4:
            crc16 = "0"+crc16
        # print "Final CRC: %s" % crc16
        s += crc16[-4:]
        check += int(crc16[:2],16) + int(crc16[-2:],16)
        file_checksum += check - 0x20
        check = ((check%256) ^ 0xffff)+1    # 2's comp
        check = hex(check)[2:]
        check = check[-2:]
        while len(check) < 2:
            check = "0"+check
        s += check
        # print s.upper()
        # Footer, clear the rest of the buffer (8 lines total)
        s += "\n:10002000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE0"
        s += "\n:10003000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD0"
        s += "\n:10004000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC0"
        s += "\n:10005000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFB0"
        s += "\n:10006000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFA0"
        s += "\n:10007000FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF90"
        s += "\n:00000001FF"
        self.file_checksum = hex(file_checksum + 255*16*6)
        return s.upper()

    ## CRC checking code stolen from somewhere...
    ##-------------------------------------------------------------------------
    ## Private
    ##    AddByteToCRC
    ##
    ## Description:
    ##    This routine calculates a CRC one byte at a time, accumulating
    ##    the result in the file static variable m_wCRC.
    ##
    ## Arguments:
    ##    Byte to be added to CRC calculation.
    ##
    ## Returns:
    ##    Nothing.
    ##
    ##-------------------------------------------------------------------------
    def AddByteToCRC(self, wData, m_wCRC):

        wData = wData << 8
##        CRC_POLY = 0x1021   # 10001000000100001
##                            # bits: 16,12,5,0
        # Poly = x^16 + x^15 + x^2 + x^0 (USB et. al.). Seed=all ones (0xFFFF).
        CRC_POLY = 0x8005   # 11000000000000101
                            # bits: 16,15,2,0
        
        for i in range(8):
            xor_flag = (m_wCRC ^ wData) & 0x8000
            m_wCRC = (m_wCRC << 1) & 0xFFFF
            if (xor_flag):
                m_wCRC = m_wCRC ^ CRC_POLY
            wData = (wData << 1) & 0xFFFF
        return m_wCRC
    
    def new(self):
        self.clear_values()

    line1 = ""
    line2 = ""
    
    def import_file(self, filename=None):
        global VERSION, current_file
        if filename == None:
            filename = tkFileDialog.askopenfilename(initialdir=".")
        if filename == "":
            return
        else:
            current_file = filename
        self.appendtext("\n\nImporting file: %s\n" % current_file)
        if current_file[-4:].lower() not in ['.hex','.mcs']:
            tkMessageBox.showerror("Invalid File Type", "Target file must be a HEX or MCS file.")
            self.appendtext("Import file failed: Target file must be a HEX or MCS file.")
            return
        file = open(current_file)
        self.line1 = file.readline()
        while self.line1[7:9] != "00" and self.line1:       # Checks if first line is a data line
            self.line1 = file.readline()
        if not self.line1:                # Returns if no line was read
            self.appendtext("\nUnexpected EOF. File import failed.")
            return
        self.line2 = file.readline()
        file.close()
        if not self.line2:                # Returns if no line was read
            self.appendtext("\nUnexpected EOF. File import failed.")
            return
        if self.line2[7:9] != "00":
            self.appendtext("\nFound nondata line where data should be. File import failed.")
            return
        if self.revert():
            # Configure titlebar to show current file
            self.master.title("PV HexGen v%s - %s" % (VERSION, current_file))
    
    def revert(self, recalcFromFile=True):
        global PODI_M, PODI_B
        self.clear_values()
        if (recalcFromFile):
            if self.line1 == "" or self.line2 == "":
                return False
            for i in range(16):
                self.values[i] = self.line1[9+i*2:11+i*2]
            for i in range(9):
                self.values[i+16] = self.line2[9+i*2:11+i*2]
        # Set the calculated GUI values
        minFSK = int(self.values[6],16)*0x100 + int(self.values[7],16)
        minFSK = (255.0/minFSK)*(2**12)
        maxFSK = int(self.values[8],16)*0x100 + int(self.values[9],16)
        maxFSK = (255.0/maxFSK)*(2**12)
        # Set Entries to show imported values
        self.entries[0].insert(END, self.values[0])
        if self.values[1] == "01":
            self.entries[1].set("Allow Max Mode")
        elif self.values[1] == "02":
            self.entries[1].set("Disable Max Mode")
        else:
            self.appendtext("\nInvalid data byte for POD_TYPE. File import failed.")
            return False
        self.minMaxV.insert(END, self.myRound(int(self.values[2],16)*FULLSCALEV / minFSK, 2))
        self.maxMaxV.insert(END, self.myRound(int(self.values[3],16)*FULLSCALEV / maxFSK, 2))
        self.minInitV.insert(END, self.myRound(int(self.values[4],16)*float(self.minMaxV.get()) / int(self.values[2],16), 2))
        self.maxInitV.insert(END, self.myRound(int(self.values[5],16)*float(self.maxMaxV.get()) / int(self.values[3],16), 2))
        self.minMaxKRPM.insert(END, int(self.values[2],16))
        self.maxMaxKRPM.insert(END, int(self.values[3],16))
        self.minFullscale.set(self.myRound(minFSK))
        self.maxFullscale.set(self.myRound(maxFSK))
        for i in range(10,12):   # External cal table
            self.entries[i].insert(END, self.myRound(PODI_M / (int(self.values[i],16) + PODI_B), 3))
        for i in range(12,16):    # 0 to 255
            self.entries[i].insert(END, int(self.values[i],16))
        for i in range(16,20):  # 0.0 to 25.5
            self.entries[i].insert(END, self.myRound(int(self.values[i],16)*(25.5/255.0), 2))
        self.entries[20].insert(END, self.myRound(int(self.values[20],16), 2))
        self.entries[21].insert(END, self.myRound(0.6/(int(self.values[21]+self.values[22],16) / 2.0**16.0), 1))
        self.entries[23].insert(END, self.myRound(int(self.values[23],16)*(22.26/255.0), 2))
        if self.values[24] == "00":
            self.entries[24].set("Normal")
        elif self.values[24] == "01":
            self.entries[24].set("Invert")
        else:
            self.appendtext("\nInvalid data byte for REX_DIRECTION. File import failed.")
            return False
        if recalcFromFile:
            self.appendtext("\nFile imported successfully")
        return True

    def close(self):
        global VERSION
        self.clear_values()
        current_file = ""
        self.master.title("PV HexGen v%s - (no file loaded)" % (VERSION))
    
    def save(self, event=None):
        global VERSION, current_file
        if current_file == "":
            self.save_as()
            return
        else:
            if not tkMessageBox.askokcancel("Overwrite file?", "Are you sure you want to overwrite the current file?\n%s" % (current_file)):
                return
        if self.check_vals():
            self.appendtext("\nWriting to file...")
            s = str(self)
            try:
                f = open(current_file, "w")
                f.write(s)
                f.close()
            except:
                self.appendtext("Failed to write to file.")
            else:
                self.appendtext("Done.\nFile successfully saved at %s" % (current_file))
                self.appendtext("\nCheckSum: %s" % (self.file_checksum))

    def save_as(self):
        global current_file
        temp = tkFileDialog.asksaveasfilename(defaultextension=".hex",
                                              initialdir=".",
                                              initialfile=current_file,
                                              )
        if temp == "":
            return
        else:
            current_file = temp
        if self.check_vals():
            self.appendtext("\nWriting to file...")
            s = str(self)
            try:
                f = open(current_file, "w")
                f.write(s)
                f.close()
            except:
                self.appendtext("Failed to write to file.")
            else:
                self.appendtext("Done.\nFile successfully saved at %s" % (current_file))
                self.appendtext("\nCheckSum: %s" % (self.file_checksum))
                self.master.title("PV HexGen v%s - %s" % (VERSION, current_file))            

    def readme(self):
        try:
            f = open("README.txt")
        except:
            return
        s = ""
        line = f.readline()
        while(line):
            s += line
            line = f.readline()
        tkMessageBox.showinfo("README",
                              s
                              )
    
    def about(self):
        global VERSION
        tkMessageBox.showinfo(
            "PV HexGen %s" % (VERSION),
            "(c) 2008 Carbon Design Inc.\nProgrammed by Ryan Vilbrandt\nLast Updated: %s" % (LAST_UPDATED)
        )

def exit_root():
    root.destroy()
    root.quit()

root = Tk()
root.title("PV HexGen v%s - (no file loaded)" % (VERSION))

# create the body
b = Body(root)

# create a menu
menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Set Values to Defaults", command=b.new)
filemenu.add_command(label="Import values from file...", command=b.import_file)
filemenu.add_command(label="Revert", command=b.revert)
filemenu.add_command(label="Close", command=b.close)
filemenu.add_separator()
filemenu.add_command(label="Save", command=b.save)
filemenu.add_command(label="Save As...", command=b.save_as)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=exit_root)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="Readme", command=b.readme)
helpmenu.add_command(label="About", command=b.about)

root.protocol("WM_DELETE_WINDOW", exit_root)

root.focus_force()
root.mainloop()
