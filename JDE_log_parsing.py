import re

def dict_replace(s, d):
    for k in d:
        s = s.replace(k, d[k])
    return s

with open("R56ZN300_MJE025100_2-7-2014.jdedebug.txt") as f:
    lines = f.readlines()

ts_reg = r"^(Feb .*?) \- "
before_reg = "\<ZonarHTTPDownload\>(.*?)\<sz\-uRL\>(.*?)\<\/sz\-uRL\>(.*?)</ZonarHTTPDownload>"
after_reg = r"<zonar-hTTPDownload\>(.*?)\<sz\-uRL\>(.*?)\<\/sz\-uRL\>(.*?)</zonar-hTTPDownload>"
return_reg = r"Return value is [^0]"

before = ""
after = ""

for line in lines:
    # Get timestamp
    m = re.search(ts_reg, line)
    if m:
        ts = m.group(1)
    # Get "before" URL
    m = re.search(before_reg, line)
    if m:
##        if before:
##            print ">>> before item had no matching after"
        before = m.group(2)
##        print "{0}: before".format(ts)
        print dict_replace(before, {"&amp;":"&", "%20":" ", "%2F":"/"})
##        print before
    # Get "after" URL
    m = re.search(after_reg, line)
    if m:
##        if not before:
##            print "<<< after item has no matching before: {0}".format(ts)
##        print "{0}: after".format(ts)
##        print ("match" if before == m.group(2) else "NO MATCH")+": {0}".format(ts)
        before = ""
    # Get Return value
##    m = re.search(return_reg, line)
##    if m:
##        print "{0}: {1}".format(ts, m.group(0))
