from random import randint

from PIL import Image

# PALETTE is a colorful option that uses the location of the pixel on the image to determine its color.as
# x will be R, y will be G, and the actual value of PALETTE will be B.

W, B, R, PALETTE = (255, 255, 255), (0, 0, 0), (255, 0, 0), 100
BITS = [W, PALETTE]   # empty, filled pixel color
LEFT_EDGE = 0   # Spoof left edge of each row as empty or filled?
RIGHT_EDGE = 0  # Spoof right edge of each row as empty or filled?
RANDOMIZE_FIRST_LINE = False
RANDOMIZE_RULES = False

class App:

    width = 4095
    height = 2048

##    rules = [1, 0, 0, 1, 1, 0, 1, 0] #frost
##    rules = [1, 0, 0, 1, 1, 1, 0, 0] #mountains
    # rules = [0, 1, 0, 0, 1, 0, 0, 0] #sierpinski
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
    
    def __init__(self):
        if RANDOMIZE_RULES:
            self.RandomizeRules()
        print(self.rules)
        print("Building array...")
        bitmap = self.BuildBitmap()
        print("Converting to colors...")
        bitmap = [[BITS[b] for b in line] for line in bitmap]
        # print bitmap
        print("Painting bitmap...")
        self.PaintBitmap(bitmap)

    def BuildBitmap(self):
        bitmap = []
        b = []
        # Setup first line
        for i in range(self.width):
            if RANDOMIZE_FIRST_LINE:
                b.append(randint(0, 1))
            else:
                if i == self.width // 2:
                    b.append(1)
                else:
                    b.append(0)
        bitmap.append(b)

        # Main
        for y in range(1, self.height):
            if y % 100 == 0:
                print("{:.0%} ({}/{} rows)".format(y / float(self.height), y, self.height))
            b = []
            # For bits at the beginning of lines, fake an upper left bit as empty if LEFT_EDGE is 0
            i = (y - 1) * self.width
            b.append(self.GetRule(LEFT_EDGE,
                                  bitmap[-1][0],
                                  bitmap[-1][1]))
            for i in range(1, self.width-1):
                b.append(self.GetRule(bitmap[-1][i - 1], bitmap[-1][i], bitmap[-1][i + 1]))
            # For bits at the end of lines, fake an upper right bit as empty if RIGHT_EDGE is 0
            i += 1
            b.append(self.GetRule(bitmap[-1][-2],
                                  bitmap[-1][-1],
                                  RIGHT_EDGE))
            bitmap.append(b)

        return bitmap

    def GetRule(self, a, b, c):
        return self.rules[(a << 2) + (b << 1) + c]

    def RandomizeRules(self):
        self.rules = [randint(0, 1) for _ in range(8)]

    def PaintBitmap(self, bitmap):
        img = Image.new('RGB', (self.width, self.height), "white")
        pixels = img.load()
        for y in range(self.height):
            # Print row
            if y % 100 == 0:
                print("{:.0%} ({}/{} rows)".format(y / float(self.height), y, self.height))
            # Set pixels
            for x in range(self.width):
                if bitmap[y][x] == PALETTE:
                    pixels[x, y] = (int((x / float(self.width)) * 256), int((y / float(self.height)) * 256), PALETTE)
                else:
                    pixels[x, y] = bitmap[y][x]
        img.show()

a = App()
