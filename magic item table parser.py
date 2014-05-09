# -*- coding: cp1252 -*-
import re

t = """Gauntlet 	2 gp 	1d2 	1d3 	x2 	— 	1 lb. 	B 	— 	CRB
Battle aspergillum 	5 gp 	1d4 	1d6 	x2 	— 	4 lb. 	B 	see text 	APG
Brass knuckles 	1 gp 	1d2 	1d3 	x2 	— 	1 lb. 	B 	monk, see text 	AA
Cestus 	5 gp 	1d3 	1d4 	19-20/x2 	— 	1 lb. 	B or P 	monk 	APG
Dagger 	2 gp 	1d3 	1d4 	19–20/x2 	10 ft. 	1 lb. 	P or S 	— 	CRB
Dagger, punching 	2 gp 	1d3 	1d4 	x3 	— 	1 lb. 	P 	— 	CRB
Gauntlet, spiked 	5 gp 	1d3 	1d4 	x2 	— 	1 lb. 	P 	— 	CRB
Mace, light 	5 gp 	1d4 	1d6 	x2 	— 	4 lbs. 	B 	— 	CRB
Sickle 	6 gp 	1d4 	1d6 	x2 	— 	2 lbs. 	S 	trip 	CRB
Wooden stake 	0 gp 	1d3 	1d4 	x2 	10 ft. 	1 lb. 	P 	— 	APG
Club 	0 gp 	1d4 	1d6 	x2 	10 ft. 	3 lbs. 	B 	— 	CRB
Club, mere 	2 gp 	1d3 	1d4 	x2 	— 	2 lbs. 	B or P 	fragile 	AA
Combat scabbard 	1 gp 	1d4 	1d6 	x2 	— 	1 lb. 	B 	improvised, see text 	AA
Mace, heavy 	12 gp 	1d6 	1d8 	x2 	— 	8 lbs. 	B 	— 	CRB
Morningstar 	8 gp 	1d6 	1d8 	x2 	— 	6 lbs. 	B and P 	— 	CRB
Shortspear 	1 gp 	1d4 	1d6 	x2 	20 ft. 	3 lbs. 	P 	— 	CRB
Bayonet 	5 gp 	1d4 	1d6 	x2 	— 	1 lb. 	P 	— 	APG
Longspear 	5 gp 	1d6 	1d8 	x3 	— 	9 lbs. 	P 	brace, reach 	CRB
Quarterstaff 	0 gp 	1d4/1d4 	1d6/1d6 	x2 	— 	4 lbs. 	B 	double, monk 	CRB
Spear 	2 gp 	1d6 	1d8 	x3 	20 ft. 	6 lbs. 	P 	brace 	CRB
Spear, boar 	5 gp 	1d6 	1d8 	x2 	— 	8 lb. 	P 	brace, see text 	APG
Axe, throwing 	8 gp 	1d4 	1d6 	x2 	10 ft. 	2 lbs. 	S 	— 	CRB
Blade boot 	25 gp 	1d3 	1d4 	x2 	— 	2 lbs. 	P 	see text 	AA
Dogslicer 	8 gp 	1d4 	1d6 	19-20/x2 	— 	1 lb. 	S 	— 	ISWG
Hammer, light 	1 gp 	1d3 	1d4 	x2 	20 ft. 	2 lbs. 	B 	— 	CRB
Gladius 	15 gp 	1d4 	1d6 	19-20/x2 	— 	3 lbs. 	P or S 	performance 	UC
Handaxe 	6 gp 	1d4 	1d6 	x3 	— 	3 lbs. 	S 	— 	CRB
Knife, switchblade 	5 gp 	1d3 	1d4 	19-20/x2 	10 ft. 	1 lb. 	P 	— 	AA
Pick, light 	4 gp 	1d3 	1d4 	x4 	— 	3 lbs. 	P 	— 	CRB
Sap 	1 gp 	1d4 	1d6 	x2 	— 	2 lbs. 	B 	nonlethal 	CRB
Starknife 	24 gp 	1d3 	1d4 	x3 	20 ft. 	3 lbs. 	P 	— 	CRB
Sword, short 	10 gp 	1d4 	1d6 	19–20/x2 	— 	2 lbs. 	P 	— 	CRB
War razor 	8 gp 	1d3 	1d4 	19-20/x2 	— 	1 lb. 	S 	— 	ISWG
Battleaxe 	10 gp 	1d6 	1d8 	x3 	— 	6 lbs. 	S 	— 	CRB
Flail 	8 gp 	1d6 	1d8 	x2 	— 	5 lbs. 	B 	disarm, trip 	CRB
Klar 	12 gp 	1d4 	1d6 	x2 	— 	6 lbs. 	S 	— 	ISWG
Longsword 	15 gp 	1d6 	1d8 	19–20/x2 	— 	4 lbs. 	S 	— 	CRB
Pick, heavy 	8 gp 	1d4 	1d6 	x4 	— 	6 lbs. 	P 	— 	CRB
Rapier 	20 gp 	1d4 	1d6 	18–20/x2 	— 	2 lbs. 	P 	— 	CRB
Scabbard, combat (sharpened) 	10 gp 	1d4 	1d6 	18-20/x2 	— 	1 lb. 	S 	see text 	AA
Scimitar 	15 gp 	1d4 	1d6 	18–20/x2 	— 	4 lbs. 	S 	— 	CRB
Scizore 	20 gp 	1d8 	1d10 	x2 	— 	3 lbs. 	P 	— 	UC
Sword cane 	45 gp 	1d4 	1d6 	x2 	— 	4 lbs. 	P 	see text 	APG
Terbutje 	5 gp 	1d6 	1d8 	19-20/x2 	— 	2 lbs. 	S 	fragile 	AA
Terbutje, steel 	20 gp 	1d6 	1d8 	19-20/x2 	— 	4 lbs. 	S 	— 	AA
Trident 	15 gp 	1d6 	1d8 	x2 	10 ft. 	4 lbs. 	P 	brace 	CRB
Warhammer 	12 gp 	1d6 	1d8 	x3 	— 	5 lbs. 	B 	— 	CRB
Bardiche 	13 gp 	1d8 	1d10 	19-20/x2 	— 	14 lbs. 	S 	brace, reach, see text 	APG
Bec de corbin 	15 gp 	1d8 	1d10 	x3 	— 	12 lbs. 	B or P 	brace, reach, see text 	APG
Bill 	11 gp 	1d6 	1d8 	x3 	— 	11 lbs. 	S 	brace, disarm, reach, see text 	APG
Earth breaker 	40 gp 	1d10 	2d6 	x3 	— 	14 lbs. 	B 	— 	ISWG
Falchion 	75 gp 	1d6 	2d4 	18–20/x2 	— 	8 lbs. 	S 	— 	CRB
Flail, heavy 	15 gp 	1d8 	1d10 	19-20/x2 	— 	10 lbs. 	B 	disarm, trip 	CRB
Glaive 	8 gp 	1d8 	1d10 	x3 	— 	10 lbs. 	S 	reach 	CRB
Glaive-guisarme 	12 gp 	1d8 	1d10 	x3 	— 	10 lbs. 	S 	brace, reach, see text 	APG
Greataxe 	20 gp 	1d10 	1d12 	x3 	— 	12 lbs. 	S 	— 	CRB
Greatclub 	5 gp 	1d8 	1d10 	x2 	— 	8 lbs. 	B 	— 	CRB
Greatsword 	50 gp 	1d10 	2d6 	19–20/x2 	— 	8 lbs. 	S 	— 	CRB
Guisarme 	9 gp 	1d6 	2d4 	x3 	— 	12 lbs. 	S 	reach, trip 	CRB
Halberd 	10 gp 	1d8 	1d10 	x3 	— 	12 lbs. 	P or S 	brace, trip 	CRB
Hammer, lucerne 	15 gp 	1d10 	1d12 	x2 	— 	12 lbs. 	B or P 	brace, reach, see text 	APG
Horsechopper 	10 gp 	1d8 	1d10 	x3 	— 	12 lbs. 	P or S 	reach, trip 	ISWG
Lance 	10 gp 	1d6 	1d8 	x3 	— 	10 lbs. 	P 	reach 	CRB
Ogre hook 	24 gp 	1d8 	1d10 	x3 	— 	10 lbs. 	P 	trip 	ISWG
Pickaxe 	14 gp 	1d6 	1d8 	x4 	— 	12 lbs. 	P 	— 	AP14
Ranseur 	10 gp 	1d6 	2d4 	x3 	— 	12 lbs. 	P 	disarm, reach 	CRB
Scythe 	18 gp 	1d6 	2d4 	x4 	— 	10 lbs. 	P or S 	trip 	CRB
Spear, syringe 	100 gp 	1d6 	1d8 	x3 	20 ft. 	6 lbs. 	P 	brace, see text 	AA"""

##print repr(t.split('\n'))

minor_dict = {}
medium_dict = {}
major_dict = {}

for i,line in enumerate(t.split('\n')):
##    temp = l[3].split(' ')
##    name = " ".join(temp[:-2])
##    pot_type = temp[-2].strip('()').title()
##    if not l[0] == '\x97 ':
##        temp = l[0].split('\x96')
    l = [x.strip(' ') for x in line.split('\t')]
    print l
    cost = int(l[1][:-3])
    crit = l[4].replace('\x96','-')
    temp = crit.split('x')
    threat_range = temp[0]
    if threat_range:
        threat_range = threat_range[:-1]
    crit_mult = int(temp[1])
    weap_type = l[7].replace(' or ',',').replace(' and ',',').split(',')
    minor_dict[i+1] = [l[0],cost,l[3],threat_range,crit_mult,weap_type]
##    if not l[1] == '\x97 ':
##        temp = l[1].split('\x96')
##        if len(temp) == 1: temp = temp*2
##        medium_dict[int(temp[1])] = [l[3],"",int(l[4][:-3].replace(',',''))]
##    if not l[2] == '\x97 ':
##        temp = l[2].split('\x96')
##        if len(temp) == 1: temp = temp*2
##        major_dict[int(temp[1])] = [l[3],"",int(l[4][:-3].replace(',',''))]
print "Minor"
print "{"+",\n         ".join([str(x)+":"+repr(minor_dict[x]) for x in sorted(minor_dict)])+"}"
##print [i*(31.0/100) for i in sorted(minor_dict)]
##print "Medium"
##print "{"+",\n".join([str(x)+":"+repr(medium_dict[x]) for x in sorted(medium_dict)])+"}"
##print "Major"
##print "{"+",\n".join([str(x)+":"+repr(major_dict[x]) for x in sorted(major_dict)])+"}"

