import re, csv

# based on the databases pulled from d20pfsrd.com
MONSTER_DB = "inputs/monster_bestiary_partial.csv"
NPC_DB = "inputs/monster_stat_blocks_full.csv"
DEMONS_DB = "inputs/demons.csv"

def print_resists(filename):
    acid_count = []
    cold_count = []
    elec_count = []
    fire_count = []
    holy_count = []
    posi_count = []
    acid_r_count = []
    cold_r_count = []
    elec_r_count = []
    fire_r_count = []
    holy_r_count = []
    posi_r_count = []
    line_count = 0
    with open(filename) as f:
        reader = csv.reader(f)        
        headers = reader.next()
##        print headers
        Name_header = headers.index("Name")
        CR_header = headers.index("CR")
        Text_header = headers.index("FullText")
        immune_reg = "<b>Immune </b>(.*?)(\;|<)"
        resist_reg = "<b>Resist </b>(.*?)(\;|<)"
        for items in reader:
            line_count += 1
##            cr = cr_to_float(items[CR_header])
##            if not (1 <= cr <= 5):
##                continue
##            print items[Name_header],"|",items[CR_header]
            m = re.search(immune_reg, items[Text_header])
            if m:
                if "acid" in m.group(1):
                    acid_count.append(items[Name_header])
                if "cold" in m.group(1):
                    cold_count.append(items[Name_header])
                if "electricity" in m.group(1):
                    elec_count.append(items[Name_header])
                if "fire" in m.group(1):
                    fire_count.append(items[Name_header])
                if "holy" in m.group(1):
                    holy_count.append(items[Name_header])
                if "posi" in m.group(1):
                    posi_count.append(items[Name_header])
            m = re.search(resist_reg, items[Text_header])
            if m:
                if "acid" in m.group(1):
                    acid_r_count.append(items[Name_header])
                if "cold" in m.group(1):
                    cold_r_count.append(items[Name_header])
                if "electricity" in m.group(1):
                    elec_r_count.append(items[Name_header])
                if "fire" in m.group(1):
                    fire_r_count.append(items[Name_header])
                if "holy" in m.group(1):
                    holy_r_count.append(items[Name_header])
                if "posi" in m.group(1):
                    posi_r_count.append(items[Name_header])

    print "Total count:",line_count
    print "Acid: Immune",len(acid_count),", Resist",len(acid_r_count)
    print "Cold: Immune",len(cold_count),", Resist",len(cold_r_count)
    print "Elec: Immune",len(elec_count),", Resist",len(elec_r_count)
    print "Fire: Immune",len(fire_count),", Resist",len(fire_r_count)
    print "Holy: Immune",len(holy_count),", Resist",len(holy_r_count)
    print "Posi: Immune",len(posi_count),", Resist",len(posi_r_count)

def cr_to_float(cr):
    cr = cr.strip(' ')
    try:
        float_cr = float(int(cr))
    except ValueError:
        try:
            split_cr = cr.partition('/')
            num = int(split_cr[0])
            den = int(split_cr[2])
            float_cr = num/float(den)
        except ValueError:
            return None
    return float_cr

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
    

print_resists(MONSTER_DB)
