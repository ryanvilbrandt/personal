import Tkinter, random
import prime_spiral

W,B,R=(255,255,255),(0,0,0),(255,0,0)
BITS = [W,R]    # empty, filled pixel color
LEFT_EDGE = 0   # Spoof left edge of each row as empty or filled?
RIGHT_EDGE = 0  # Spoof right edge of each row as empty or filled?
RANDOMIZE_FIRST_LINE = False
RANDOMIZE_RULES = False

class App:

    width = 300
    height = width
    
    def __init__(self, t):
        self.i = Tkinter.PhotoImage(width=self.width,height=self.height)
        print "Building array..."
        bitmap1 = prime_spiral.build_spiral(self.width)
##        print bitmap1
        print "Converting to colors..."
        bitmap2 = []
        for i in bitmap1:
            a = []
            for j in i:
                if j == 1:
                    a.append(R)
                elif j == "X":
                    a.append(B)
                else:
                    a.append(W)
            bitmap2 += a
##        print bitmap2
        print "Painting bitmap..."
        self.PaintBitmap(bitmap2)

    def PaintBitmap(self, bitmap):
        row = 0
        col = 0
        for j,bit in enumerate(bitmap):
           self.i.put('#%02x%02x%02x' % tuple(bit),(col,row))
           col += 1
           if col == self.width:
               if row % 100 == 0:
                   print "{0:.0%} ({1}/{2} rows)".format(row/float(self.height),row,self.height)
               row +=1; col = 0        
        c = Tkinter.Canvas(t, width=self.width, height=self.height)
        c.pack()
        c.create_image(0, 0, image = self.i, anchor=Tkinter.NW)

t = Tkinter.Tk()
a = App(t)    
t.mainloop()
