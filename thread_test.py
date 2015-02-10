import threading

RunThreads = True
l = [None, None, None, None, None, None, None, None, None, None]

def MoveForward():
    global l
##    while(RunThreads):
    for i in xrange(10):
        l[i] = 0
        print 'Forward:  '+str(l)+'\n',

def MoveBackward():
    global l
##    while(RunThreads):
    for i in xrange(1,11):
        l[-i] = 1
        print 'Backward: '+str(l)+'\n',


t = threading.Thread(name="Forward", target=MoveForward)
t2 = threading.Thread(name="Backward", target=MoveBackward)
t.start()
t2.start()

try:
    while(RunThreads): pass
except KeyboardInterrupt:
    RunThreads = False
