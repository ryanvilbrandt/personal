import os

print os.environ
print ""
##print os.environ["ALLUSERSPROFILE"]
##print os.environ["USERPROFILE"]
##print os.environ["APPDATA"]

def write_test(path):
    with open(os.path.join(path,"test.txt"),"w") as f:
        f.write("testing 123")


paths = ["ALLUSERSPROFILE", "USERPROFILE", "APPDATA"]

for p in paths:
    print ""
    print p
    if not p in os.environ:
        print "No os.environ entry for {0}".format(p)
    else:
        print os.environ[p]
        try:
            write_test(os.environ[p])
        except Exception as e:
            print "Couldn't write to {0}: {1}".format(os.environ[p], e)
        else:
            print "SUCCESS"


raw_input("Press ENTER to continue...")
