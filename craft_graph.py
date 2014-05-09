import numpy as np
import matplotlib
import matplotlib.cm as cm
import matplotlib.pyplot as plt

SP, GP = 0, 1
DAY, WEEK = 0, 1

##ax1 = plt.subplot(2,2,1)
##cb = plt.colorbar() #1
##cb.set_label('counts')
##ax2 = plt.subplot(2,2,2)
##cb = plt.colorbar()
##cb.set_label('counts')
##ax3 = plt.subplot(2,2,3)
##cb = plt.colorbar()
##cb.set_label('counts')
##ax4 = plt.subplot(2,2,4)
##cb = plt.colorbar()
##cb.set_label('counts')
##ax.plot([0,11],[0,300],' ') # Set size of window

def MakeItem(skill=5,dc=10,price=1000,denom=SP,interval=WEEK):
    if dc > skill + 20:
        return None
    progress = 0
    cost = price / 3.0
    time = 0    # All time is recorded in days
##    print skill,dc,price,denom,interval
    while (progress < cost):
        d = np.random.random_integers(20)+skill
        if d <= dc - 5:
            temp = price / 6.0
##            if interval == DAY:
##                temp = temp / 7.0
            cost += temp
        elif d >= dc:
            temp = d*dc
            if interval == DAY:
                temp = temp / 7.0
            progress += temp
        time += 1
        if cost > price*2:
##            time,cost = 0,0
            break
##    if interval == DAY:
##        time /= 7.0
    return time,cost

def Draw3Plot(s,d,p,i,clr,plt1,plt2,plt3):
    iterations = 10000
    l = [MakeItem(skill=s, dc=d, price=p, interval=i) for each in range(iterations)]
    x,y = zip(*l)
##    print x,y
    day_week = ((not i and "day") or (i and "week"))
    print help(plt1.plot)
    plt1.plot(x, y, clr)
    plt1.set_title("Time ({0}) vs. Cost ({1}) prob of making a single item\nS={2} DC={3} P={4} I={0}".format(day_week,"sp",
                                                                                                             s,d,p))

    l = list(set(x))
    n = [x.count(j) for j in l]
##    print "Time:",l,n
    plt2.plot(l, n, clr)
    plt2.set_title("# of results for a given time to craft ({0})".format(day_week))

    l = list(set(y))
    n = [y.count(j) for j in l]
##    print "Cost:",l,n
    plt3.plot(l, n, clr)
    plt3.set_title("# of results for a given cost to craft ({0})".format("sp"))

    if sum(x):
        print "Profit per day:", str((p*iterations-sum(y))/sum(x))
    else:
        print "No profit"

def ProfitPlot(s,d,p,i,clr,plt):
    profits = []
    indic = []
    for j in xrange(21):
        iters = 10000
        l = [MakeItem(skill=s, dc=d, price=p, interval=i) for each in range(iters)]
        x,y = zip(*l)
        
        profits.append((p*iters-sum(y))/sum(x))
        print "Profit per day:", str(profits[-1])
        indic.append(d)

        # If DC is 20 greater than skill, stop calculating
        if d >= s + 20: break
        ## Change between attempts here
        d+=1

    plt.plot(indic, profits, clr)
    print ""
        
y = 3
x = 1
plt.subplots_adjust(hspace=0.5)
plots = [plt.subplot(y,x,i) for i in range(1,y*x+1)]

s=8
p=15000
i=WEEK
d=19
colors = ['r.', 'g.', 'b.', 'm.', 'y.', 'c.', 'k.']
##plots[0].set_title("Profits (sp/day vs DC vs price) | skill={0}, price={1}sp, DC={2}, per {3}".format(s,p,d,(not i and "day")or(i and "week")))

##for c in colors:
##    ProfitPlot(s,d,p,i,c,plots[0])
##    p+=500

for j in xrange(x):
    Draw3Plot(s,d,p,i,colors[j],plots[j],plots[j+x],plots[j+x+x]) # Needs y=3
    s+=5

##Draw3Plot(s,d,p,i,colors[0],plots[1],plots[3],plots[0]) # Needs x=2,y=2


plt.show()
