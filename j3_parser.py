import re, time

reg = r"\d\d \d\d\:\d\d\:\d\d\t(*.?)"

def str_to_elapsed(s,t):
    a = int(s[6:8])*60+int(s[9:11])
    b = int(t[6:8])*60+int(t[9:11])
    c = b-a
    if c < 0:
        c += 3600
    return time.strftime("%Mm %Ss",time.gmtime(c))

with open("j3_sim log.txt","r") as f:
    with open("j3_sim parsed log.csv","w") as g:
        truck_on = False
        time_elapsed = ""
        for line in f.readlines():
            if line[12:] == "DEBUG: '$Linked to PUMP'\n":
                if truck_on:
                    g.write("{0},{1},\n".format(line[:11],line[:11]))
                truck_on = True
                time_elapsed = line[:11]
            if line[12:] == "DEBUG: '$PUMP Communication Timeout.'\n":
                truck_on = False
                g.write("{0},{1},\n".format(line[:11],
                                            str_to_elapsed(time_elapsed,line[:11])))
    
