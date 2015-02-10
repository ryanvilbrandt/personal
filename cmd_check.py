import re, csv

# based on the databases pulled from d20pfsrd.com
MONSTER_DB = "inputs/monster_bestiary_partial.csv"
NPC_DB = "inputs/monster_stat_blocks_full.csv"

def get_cmd(filename):
    hit_d = {}
    cmd_d = {}
    with open(filename) as f:
        reader = csv.reader(f)        
        headers = reader.next()
        print headers
        Name_header = headers.index("Name")
        CR_header = headers.index("CR")
        Melee_header = headers.index("Melee")
        CMD_header = headers.index("FullText")
        hit_reg = ".((\+|\-)?\d+)"
        cmd_reg = "<b>CMD </b>(\<i\>)?(\+?\d+|\-)"
        for items in reader:
            if items[Melee_header]:
                m = re.search(hit_reg, items[Melee_header])
                try:
    ##                print "{0}|{1}|{2}".format(items[Name_header],
    ##                                           items[Melee_header],
    ##                                           m.group(1))
                    hit = int(m.group(1))
                    a = hit_d.get(items[CR_header], [])
                    if a == None:
                        print hit_d
                        return
                    a.append(hit)
                    hit_d[items[CR_header]] = a
                except Exception as e:
                    print "Hit:",items[Name_header],e
                    print "\t",items[Melee_header]
    ##                print m.groups()
    ##                return
            m = re.search(cmd_reg, items[CMD_header])
            try:
                if m.group(2) != '-':
                    cmd = int(m.group(2))
                    a = cmd_d.get(items[CR_header], [])
                    if a == None:
                        print cmd_d
                        return
                    a.append(cmd)
                    cmd_d[items[CR_header]] = a
            except Exception as e:
                print "CMD:",items[Name_header],e

    return hit_d, cmd_d

def mean(l):
    return float(sum(l))/len(l)

def median(numericValues):
  theValues = sorted(numericValues)

  if len(theValues) % 2 == 1:
    return theValues[(len(theValues)+1)/2-1]
  else:
    lower = theValues[len(theValues)/2-1]
    upper = theValues[len(theValues)/2]

    return (float(lower + upper)) / 2

def mode(alist):
    mode = None
    mode_count = 0
    no_dups = list(set(alist))
    for i in no_dups:
##        print i,alist.count(i)," ",
        if alist.count(i) > mode_count:
            mode = i
            mode_count = alist.count(i)
##    print ""
    return mode, mode_count, "{0:.1%}".format(float(mode_count)/len(alist))

def stddev(l, m=None):
    if not m:
        m = mean(l)
    stddev_l = [(m-n)**2 for n in l]
    return mean(stddev_l)**0.5             

def print_avgs(d):
    keys = sorted(d.keys())
    for k in keys:
        print "{0}\t{1}\t{2}".format(k, mean(d[k]), stddev(d[k]))
    

hit_d, cmd_d = get_cmd(MONSTER_DB)
print hit_d
print cmd_d
print ""
print "To hit:"
print_avgs(hit_d)
print ""
print "CMD:"
print_avgs(cmd_d)
