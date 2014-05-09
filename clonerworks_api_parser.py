import urllib2, json

type_dict = {}
with open("typeids.csv", "r") as f:
    for line in f:
        s = line.strip('\n').split(',')
        type_dict[s[1]] = int(s[0])

print "Paste the desired item names here, one to each line:"
r = raw_input()
##r = "EMP S"
print ""

def ConvertToPerfect(mat, waste=0.10):
    return int((mat/(1+waste))+0.5)

for item in r.split('\n'):
    if not item.endswith("Blueprint"):
        bp = item + " Blueprint"
        if bp in type_dict:
            url = "http://api.clonerworks.com/api/blueprint-calc/{0}".format(type_dict[item])
            req = urllib2.Request(url)
            opener = urllib2.build_opener()
            try:
                f = opener.open(req)
            except Exception as e:
                print "{0}\t{1}".format(item,e)
            else:
                j = json.load(f)
                f.close()
                # Name
                s = j['bpDetails']['typeName'] + '\t'

                # Base materials
                base_d = {}
                materials = ['Tritanium', 'Pyerite', 'Mexallon', 'Isogen', 'Nocxium', 'Zydrine', 'Megacyte', 'Morphite']
                for mat in j['materials']['baseMaterials']:
                    if mat:
                        base_d[mat['typeName']] = ConvertToPerfect(mat['amount'])
                for m in materials:
                    if m in base_d:
                        s += str(base_d[m]) + '\t'
                    else:
                        s += '0\t'

                # Extra materials
                extra_d = {}
                for mat in j['materials']['extraMaterials']:
                    if mat:
                        extra_d[mat['typeName']] = mat['amount']
                for m in materials:
                    if m in extra_d:
                        s += str(extra_d[m]) + '\t'
                    else:
                        s += '\t'

                # Quantity produced per run
                s += str(j['bpDetails']['portionSize']) + '\t'

                # Market ID
                print s + str(type_dict[item])
    
