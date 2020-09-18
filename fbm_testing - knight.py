import urllib2, time
import xml.etree.ElementTree as ET

# Set values here to control the behavior of the script below
INBOUND, OUTBOUND, ACK = 0, 1, 2
DIRECTION = INBOUND
##DIRECTION = OUTBOUND
##DIRECTION = ACK
FORM = 40
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

inbound_url_template = ("http://nealdev3.zonarsystems.net/interface.php?username=ryan.v&password=[-p0o9i8"+
                        "&action=twentytwenty&operation=sendmessage&format=xml&version=2&target=6344"+
                        "&reqtype=dbid&form={0}&provider=knight_ies&customer=dbr47_rep1023&messageid={1}&data=|{2}|")
outbound_url_template = ("http://nealdev3.zonarsystems.net/interface.php?username=ryan.v&password=[-p0o9i8"+
                         "&action=twentytwenty&operation=getmessages&format=xml&version=2"+
                         "&customer=dbr47_rep1023&start={0}&provider=mcleod")
ack_url_template = ("http://nealdev3.zonarsystems.net/interface.php?username=ryan.v&password=[-p0o9i8"+
                    "&action=twentytwenty&operation=getacks&format=xml&version=2&customer=dbr47_rep1023"+
                    "&start={0}&provider=MCleod")

# FromDispatch data sets, for Inbound messages
forms = {40: ("000YM001222222  8521988        2014021423373804010NNB00000004687870       043265900MACYS LOGISTICS-GOODYEAR "+
             "16575 WEST COMMERCE DR                            GOODYEAR ,AZ             623-925-376812/06 07:0012/06 "+
             "07:00                    N00000000000N11807202                                        MACY'S (LOCAL)           "+
             "15541 GALE AVE           OR 24/7                  CITY OF INDUSTR ,CA      678-406-720412/06 15:0012/06 "+
             "23:59BD0034200000                           SEAL INTEGRITY IS CRITICAL DO NOT LEAVE WITH OUT SEAL IN TACT "+
             "WRITTEN ON BOLS @ ALL PU/DELSTOP#1 TRAILER: STOP#2 TRAILER:")
         }

def SendHttpMessage(url):
##    print URL
    req = urllib2.Request(url)
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
        url = inbound_url_template.format(FORM, int(time.time()), urllib2.quote(forms[FORM]))
        print SendHttpMessage(url)
    elif DIRECTION == OUTBOUND:
        print "Checking for driver messages..."
        epoch = int(time.time()) - HISTORY_LENGTH
        url = outbound_url_template.format(epoch)
        response = SendHttpMessage(url)
        PrintOutboundMessages(response)
    elif DIRECTION == ACK:
        print "Checking for ack messages..."
        epoch = int(time.time()) - HISTORY_LENGTH
        url = ack_url_template.format(epoch)
        response = SendHttpMessage(url)
        PrintAckMessages(response)
