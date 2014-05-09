import urllib, urllib2, time
import xml.etree.ElementTree as ET

##USERNAME = "mcleod"
##PASSWORD = "qatest"
USERNAME = "XXXXXX"
PASSWORD = "XXXXXX"
SERVER = "nealdev3"
ACCOUNT = "dbr47_rep1023"
##SERVER = "qa1"
##ACCOUNT = "mbl2020"
DRIVER_ID = "6344"
##PROVIDER = "mcleod"
PROVIDER = "totalmail"
FORM = 12
# Set values here to control the behavior of the script below
INBOUND, INBOUND_DATA, OUTBOUND, ACK, TEST = 0, 1, 2, 3, 4
##DIRECTION = INBOUND
##DIRECTION = INBOUND_DATA
##DIRECTION = OUTBOUND
DIRECTION = ACK
##DIRECTION = TEST
# Time interval from present to check for outbound/ack messages
# 600 = all messages up to 10 minutes in the past
HISTORY_LENGTH = 6000



def fill(num):
    '''
    Creates a string based on max length, with trailing ~~.
    Useful for determining if the 2020 form can hold the max length of characters.
    '''
##    return "W"*num+"~~"
    return "".join([str(i % 10) for i in xrange(num)])+"~~"

inbound_url_template = ("https://{server}.zonarsystems.net/interface.php?username={username}&password={password}"+
                        "&action=twentytwenty&operation=sendmessage&format=xml&version=2&target={driver_id}"+
                        "&reqtype=dbid&form={form}&provider={provider}&customer={account}&messageid={message_id}&data=|{data}|")
inbound_url_template_short = "https://{server}.zonarsystems.net/interface.php"
inbound_url_data = {"username":USERNAME, "password":PASSWORD, "action":"twentytwenty", "operation":"sendmessage",
                    "format":"xml", "version":"2", "target":DRIVER_ID, "reqtype":"dbid", "form":"0",
                    "provider":PROVIDER, "customer":ACCOUNT, "messageid":0, "data":"test"}
outbound_url_template = ("https://{server}.zonarsystems.net/interface.php?username={username}&password={password}"+
                         "&action=twentytwenty&operation=getmessages&format=xml&version=2"+
                         "&customer={account}&start={start}&provider={provider}")
ack_url_template = ("https://{server}.zonarsystems.net/interface.php?username={username}&password={password}"+
                    "&action=twentytwenty&operation=getacks&format=xml&version=2&customer={account}"+
                    "&start={start}&provider={provider}")

# FromDispatch data sets, for Inbound messages
forms = {0: ["Python test to ryan"],
         1: [fill(12), fill(8), fill(24), fill(22), fill(29), fill(38), fill(12), fill(5), fill(5), fill(5), fill(5),
             fill(29), fill(38), fill(4), fill(5), fill(2), fill(2), fill(2), fill(22), fill(29), fill(38), fill(12),
             fill(5), fill(5), fill(5), fill(5), fill(38), fill(4), fill(38), fill(38), fill(38), fill(38)],
##         1: [fill(12), fill(8), fill(24), fill(22), fill(29), fill(38),
##             fill(20), "Jan01", "00:00", "Dec31", "23:59", fill(29), fill(38), "15kg", "35lbs",
##             "99", "00", "11", fill(22), fill(29), fill(38), fill(20), "Jan01", "00:00",
##             "Dec31", "23:59", fill(38), "1234",
##             fill(38), fill(38), fill(38), fill(38)],
         2: [fill(10), fill(2), fill(30), fill(24), fill(2), fill(5), fill(5), fill(5), fill(5), fill(30), fill(28), fill(24),
             fill(2), fill(5), fill(5), fill(5), fill(5), fill(4), fill(4)],
##         2: ["Butt Dimes", "22", "Ship My Tookus - International", "Istanbul, not Constantinople", "WA", "Jan01", "00:00",
##             "Dec31", "23:59", "Hickory smoked horse buttholes", "IIiiII Will Always Love Yooou!", "Actually Constantinople!", "XX", 
##             "Jan01", "00:00", "Dec31", "23:59", "9999", "0000"],
         3: [fill(26), fill(4), fill(5), fill(5), fill(30), fill(38), fill(29), fill(38)],
         4: [fill(10)],
         5: [fill(26), fill(10), fill(10), fill(35), fill(10), fill(5), fill(5), fill(24), fill(2)],
         6: [fill(29), fill(30), fill(24), fill(2), fill(12), fill(38), fill(38), fill(38), fill(38)],
         7: [fill(10), fill(11), fill(5), fill(8), fill(8), fill(4), fill(4)],
         8: [fill(30), fill(3), fill(22), fill(29), fill(38)],
         9: [fill(10), fill(7), "3", fill(34), "N", fill(23), fill(29), fill(38)],
         10: [fill(32), fill(28), fill(8)],
         11: [""],
##         12: [fill(5), fill(5), fill(6), fill(24), fill(2), fill(31), fill(38)],
         12: [fill(5), fill(5), fill(5), fill(5), fill(5), fill(5), fill(5)],
         }

def SendHttpMessage(url, data=None, proxy=None):
##    print url
    if not proxy == None:
        proxy_support = urllib2.ProxyHandler(proxy)
        opener = urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
    if data:
        d = urllib.urlencode(data)
        req = urllib2.Request(url, d)
    else:
        req = urllib2.Request(url)
    print req.data
    res = urllib2.urlopen(req)
    return res.read()

def PrintOutboundMessages(xml):
    '''
    Takes a list of FromDriver OMI messages (XML string) and prints each message
    @param xml (str)
    '''
    tree = ET.fromstring(xml)
    print "Retrieved on {0}".format(time.ctime(int(tree.attrib['timestamp'])))
    print ""
    for message in tree:
        print "Message sent on {0}".format(time.ctime(int(message.find('timestamp').text)))
        print ET.tostring(message)

def PrintAckMessages(xml):
    '''
    Takes a list of FromDriver OMI messages (XML string) and prints each message
    @param xml (str)
    '''
    tree = ET.fromstring(xml)
    print "Retrieved on {0}".format(time.ctime(int(tree.attrib['timestamp'])))
    print ""
    for message in tree:
        print "Message sent on {0}".format(time.ctime(int(message.find('timestamp').text)))
        # Each message sent from McLeod has a message_id, that lets them pair ACKs with sent messages.
        # Currently using timestamps as the message_id for testing
        print "Matches message {0} sent on".format(message.attrib['messageid']),
        # Try block may not be useful in production, depending on what format Mcleod uses.
        try:
            print time.ctime(float(message.attrib['messageid']))
        except Exception as e:
            print ""
        print ET.tostring(message)

if __name__ == "__main__":
    if DIRECTION == INBOUND:
        print "Sending Form {0}: {1}".format(FORM, forms[FORM])
        # Make the form URL safe before sending it with urllib2.quote
        url = inbound_url_template.format(username=USERNAME, password=PASSWORD, server=SERVER,
                                          form=FORM, account=ACCOUNT, driver_id=DRIVER_ID,
                                          message_id=int(time.time()), provider=PROVIDER,
                                          data=urllib2.quote("|".join(forms[FORM])))
        print url
        print SendHttpMessage(url, proxy={'https': "localhost:8008"})
    elif DIRECTION == INBOUND_DATA:
        print "Sending Form {0}: {1}".format(FORM, forms[FORM])
        # Make the form URL safe before sending it with urllib2.quote
        d = inbound_url_data
        d["messageid"] = int(time.time())
        d["form"] = FORM
        d["data"] = "|".join(forms[FORM])
        if PROVIDER == "mcleod":
            d["data"] = "|"+d["data"]+"|"
        print SendHttpMessage(inbound_url_template_short.format(server=SERVER),
                              data=d, proxy={'https': "localhost:8008"})
    elif DIRECTION == OUTBOUND:
        print "Checking for driver messages..."
        epoch = int(time.time()) - HISTORY_LENGTH
        url = outbound_url_template.format(username=USERNAME, password=PASSWORD,
                                           server=SERVER, account=ACCOUNT,
                                           start=epoch, provider=PROVIDER)
        print url
        response = SendHttpMessage(url)
        PrintOutboundMessages(response)
    elif DIRECTION == ACK:
        print "Checking for ack messages..."
        epoch = int(time.time()) - HISTORY_LENGTH
        url = ack_url_template.format(username=USERNAME, password=PASSWORD,
                                      server=SERVER, account=ACCOUNT,
                                      start=epoch, provider=PROVIDER)
        print url
        response = SendHttpMessage(url)
        PrintAckMessages(response)
    elif DIRECTION == TEST:
        for k in forms:
            url = inbound_url_template.format(username=USERNAME, password=PASSWORD, server=SERVER,
                                              form=k, account=ACCOUNT, driver_id=DRIVER_ID,
                                              message_id=int(time.time()),
                                              data=urllib2.quote("|".join(forms[k])))
            print url
        epoch = int(time.time()) - HISTORY_LENGTH
        url = outbound_url_template.format(username=USERNAME, password=PASSWORD,
                                           server=SERVER, account=ACCOUNT,
                                           start=epoch)
        print url
        url = ack_url_template.format(username=USERNAME, password=PASSWORD,
                                      server=SERVER, account=ACCOUNT,
                                      start=epoch)
        print url
        
