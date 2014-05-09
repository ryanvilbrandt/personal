import numpy as np
import matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as plt

SP, GP = 0, 1
DAY, WEEK = 0, 1

def MakeItem(skill=5,dc=10,price=1000,denom=SP,interval=WEEK):
    progress = 0
    cost = price // 3
    time = 0
    while (progress < price):
        d = np.random.random_integers(20)+skill
        if d <= dc - 5:
            temp = price // 3
            if interval == DAY:
                temp = temp//7
            cost += temp
        elif d >= dc:
            temp = d*dc
            if interval == DAY:
                temp = temp//7
            progress += temp
        time += 1
    if interval == WEEK:
        time *= 7.0
    return time,cost

m = 2
n = 2
ss=[8,9,10,9]
d=[15]*m*n
p=[350]*m*n
i=[DAY]*m*n

plt.subplots_adjust(hspace=0.5)

for j in range(m*n):
    plt.subplot(m,n,j+1)
    l = [MakeItem(skill=ss[j], dc=d[j], price=p[j], interval=i[j])
         for each in range(10)]
    x,y = zip(*l)
    print x,y
    # hexbin hates when all values in y are the same. Dumb algorithm.
    plt.hexbin(x,y, mincnt=1, gridsize=30, cmap=cm.jet)
    plt.axis([min(x)-1, max(x)+1, min(y)-10, max(y)+10])
    plt.title("S={} DC={} P={} I={}".format(ss[j],d[j],p[j],i[j]))
##    cb = plt.colorbar()
##    cb.set_label('counts')
    print j+1,

plt.show()
