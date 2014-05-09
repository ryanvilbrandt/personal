import threading, time

run_threads = True
print_buffer = []
buffer_lock = False

def get_buffer_lock():
    global run_threads
    # if the buffer is locked, wait
    while buffer_lock and run_threads:
        pass
    if not run_threads:
        return False
    return True

def release_buffer_lock():
    buffer_lock = False

def handle_buffer():
    global run_threads, print_buffer
    while run_threads:
        # Put lock on the buffer and save to local
        # Empty buffer and unlock
        time.sleep(1)
        if not get_buffer_lock(): return
        temp = print_buffer
        print_buffer = []
        release_buffer_lock()
        # Print each line to output as one big string
        # split by newlines
        print "".join(print_buffer)

def quick_print(t):
    if not get_buffer_lock(): return
    print_buffer.append(t)
    release_buffer_lock()
        
if __name__ == "__main__":
    try:
        runs = 1000
        
        clock_time = time.clock()
        t = threading.Thread(name="handle buffer", target=handle_buffer)
        t.start()
        for x in xrange(runs):
            quick_print("This is a test: {0}".format(x))

        quick_end_time = time.clock() - clock_time


        clock_time = time.clock()
        for x in xrange(runs):
            print("This is a test: {0}".format(x))

        end_time = time.clock() - clock_time
        print "Quick print took {0} seconds.".format(quick_end_time)
        print "Normal print took {0} seconds.".format(end_time)
    except KeyboardInterrupt:
        pass
    run_threads = False
    print "Threads ended"
