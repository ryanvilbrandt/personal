from Tkinter import Tk, Canvas, PhotoImage, mainloop
from random import randint, choice
import threading

WIDTH, HEIGHT = 1200, 900
ITERS = 50001

def DrawImage(img):
    # Determine the vertices
    a = WIDTH // 2
    temp = int((HEIGHT-3) // (3**0.5))
    b = a-temp
    c = a+temp
    array = ((a,2), (b,HEIGHT-1), (c,HEIGHT-1))
##    for x in array:
##        img.put("#0000AA", x)
    
    # Determine first point randomly within the triangle
    y = randint(2,HEIGHT-2)
    d = y//3**0.5
    x = randint(a-d, a+d)
    p = (x,y)

    # Pick a point halfway between p and one random vertice.
    # Color that point and make it p
    # Repeat
    for i in xrange(ITERS):
        if i % 10000 == 0: print "{0} / {1} ({2:.0%})".format(i,ITERS,float(i)/ITERS)
        v = choice(array)
        p = (int((p[0]+v[0])//2), int((p[1]+v[1])//2))
        img.put("#FF0000", p)

window = Tk()
canvas = Canvas(window, width=WIDTH, height=HEIGHT, bg="#ffffff")
canvas.pack()
img = PhotoImage(width=WIDTH, height=HEIGHT)
canvas.create_image((WIDTH/2, HEIGHT/2), image=img, state="normal")

##t = threading.Thread(name="DrawImage", target=DrawImage, args=(img))
##t.start()
DrawImage(img)

mainloop()
