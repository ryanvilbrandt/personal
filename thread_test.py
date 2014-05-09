import threading

RunThreads = True
l = [None, None, None, None, None, None, None, None, None, None]

def MoveForward():
    global l
##    while(RunThreads):
    for i in xrange(10):
        l[i] = 0

def MoveBackward():
    global l
##    while(RunThreads):
    for i in xrange(1,11):
        l[-i] = 1
        print l


t = threading.Thread(name="Forward", target=MoveForward)
t.start()
t = threading.Thread(name="Backward", target=MoveBackward)
t.start()

try:
    while(RunThreads): pass
except KeyboardInterrupt:
    RunThreads = False
