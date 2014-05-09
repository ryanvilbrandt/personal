import Tkinter, random

W,B,R=(255,255,255),(0,0,0),(255,0,0)
BITS = [W,R]    # empty, filled pixel color
LEFT_EDGE = 0   # Spoof left edge of each row as empty or filled?
RIGHT_EDGE = 0  # Spoof right edge of each row as empty or filled?
RANDOMIZE_FIRST_LINE = False
RANDOMIZE_RULES = False

class App:

    width = 20
    height = 10

##    rules = [1, 0, 0, 1, 1, 0, 1, 0] #frost
##    rules = [1, 0, 0, 1, 1, 1, 0, 0] #mountains
##    rules = [0, 1, 0, 0, 1, 0, 0, 0] #sierpinski
    rules = [0, 1, 1, 0, 1, 0, 0, 0] #sierpinski2
##    rules = [1, 0, 1, 0, 0, 1, 0, 1] #raindrops
##    rules = [1, 1, 0, 1, 0, 0, 0, 0] #wrinkles
##    rules = [0, 1, 1, 0, 1, 1, 0, 0] #waterlines
##    rules = [1,     #000
##             0,     #001
##             0,     #010
##             0,     #011
##             0,     #100
##             0,     #101
##             0,     #110
##             1,     #111
##             ]
    
    def __init__(self, t):
        self.i = Tkinter.PhotoImage(width=self.width,height=self.height)
        if RANDOMIZE_RULES:
            self.RandomizeRules()
        print self.rules
        print "Building array..."
        bitmap = self.BuildBitmap()
        print "Converting to colors..."
        bitmap = [[str(BITS[b]) for b in line]
                  for line in bitmap]
        print bitmap
        print "Painting bitmap..."
        self.PaintBitmap(bitmap)

    def BuildBitmap(self):
        bitmap = []
        b = []
        # Setup first line
        for i in xrange(self.width):
            if RANDOMIZE_FIRST_LINE:
                b.append(random.randint(0,1))
            else:
                if i == self.width // 2:
                    b.append(1)
                else:
                    b.append(0)
        bitmap.append(b)

        # Main
        for y in xrange(1, self.height):
            b = []
            # For bits at the beginning of lines,
            # fake an upper left bit as empty
            # if LEFT_EDGE is 0
            i = (y-1)*self.width
            b.append(self.GetRule(LEFT_EDGE,
                                  bitmap[-1][0],
                                  bitmap[-1][1]))
            for i in xrange(1,self.width-1):
##                i = (y-1)*self.width + x
##                print y,x,i
                b.append(self.GetRule(bitmap[-1][i-1], bitmap[-1][i], bitmap[-1][i+1]))
            # For bits at the end of lines,
            # fake an upper right bit as empty
            # if RIGHT_EDGE is 0
            i += 1
            b.append(self.GetRule(bitmap[-1][-2],
                                  bitmap[-1][-1],
                                  RIGHT_EDGE))
            bitmap.append(b)

        return bitmap

    def GetRule(self, a, b, c):
        return self.rules[(a<<2) + (b<<1) + c]

    def RandomizeRules(self):
        self.rules = [random.randint(0,1) for i in xrange(8)]

    def PaintBitmap(self, bitmap):
        row = 0
        col = 0
        for bit in bitmap:
            print bit
            self.i.put("{" + " ".join(bit) + "}")
##           self.i.put('#%02x%02x%02x' % tuple(bit),(col,row))
##           col += 1
##           if col == self.width:
##               if row % 100 == 0:
##                   print "{0:.0%} ({1}/{2} rows)".format(row/float(self.height),row,self.height)
##               row +=1; col = 0        
        c = Tkinter.Canvas(t, width=self.width, height=self.height)
        c.pack()
        c.create_image(0, 0, image = self.i, anchor=Tkinter.NW)

t = Tkinter.Tk()
a = App(t)    
t.mainloop()
