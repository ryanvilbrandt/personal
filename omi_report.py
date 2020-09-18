import urllib2, time
import xml.etree.ElementTree as ET
##import xml.etree.ElementTree

url = "https://kra0457.zonarsystems.net/interface.php?username=zonar&password=fogbank12&action=showopen&operation=showassets&reqtype=dbid&target=4328&format=xml"

# Edit asset
# Remove GPS ID from trailer
# Gets all attributes assigned to asset
# Deletes attributes from the system
# Reassign attributes to the asset
# Set custom fields

base_url = "https://qa1.zonarsystems.net/interface.php?customer=MJE0796&username=jde_integration&password=integrate1234&"
att_assign = [119, 128, 1180, 443, 545, 984, 48, 1123, 1124, 51, 77, 1108, 1014]
arguments = {"edit": [('action', 'adminassets'), ('operation', 'edit'), ('format', 'xml'), ('reqtype', 'dbid'),
                      ('version', '2'), ('target', '1118'), ('name', 'A006345'), ('fleet', '2510919'), ('exsid', '18745'),
                      ('location', '25162005232'), ('type', 'TRAILER'), ('newtype', 'TRAILER'), ('vin', 'MJE0390919'),
                      ('tagid', '79600533'), ('mfg', '.'), ('mileageoffset', '0'), ('engine_hour_offset', '0'),
                      ('subtype', '180-Trailers%20-%20Specialty'), ('status', '1')],
             "editgps": [('action', 'adminassets'), ('operation', 'editgps'), ('format', 'xml'), ('reqtype', 'exsid'),
                         ('target', '18745'), ('gpsunit', '')],
             "showassets": [('action', 'showopen'), ('operation', 'showassets'), ('format', 'xml'), ('reqtype', 'dbid'), ('target', '1118')],
             "list": [('action', 'adminattributeassign'), ('operation', 'list'), ('format', 'xml'), ('type', '1'), ('target', '1118')],
             "delete": [('action', 'adminattributeassign'), ('operation', 'delete'), ('format', 'xml'), ('target', '{0}')],
             "add": [('action', 'adminattributeassign'), ('operation', 'add'), ('format', 'xml'), ('rtypeid', '1'), ('aid', '{0}'), ('rid', '1118')],
             "editcustom1": [('action', 'adminassets'), ('operation', 'editcustomdata'), ('format', 'xml'), ('reqtype', 'exsid'),
                             ('labelid', '3'), ('target', '18745'), ('labelval', '89%20Pole%2FMaterial%20Trl%20%20%20%20%20%20%20%20%20%20')],
             "editcustom2": [('adminassets',), ('operation', 'editcustomdata'), ('format', 'xml'), ('reqtype', 'exsid'),
                             ('labelid', '4'), ('target', '18745'), ('labelval', '180-Pole%20Trl')]
             }
             

def send_omi_call(url, operation):
    if url == "": return True
    
    print operation
    print url
    # Create URL file object
    try:
        req = urllib2.Request(url)
        f = urllib2.urlopen(req)
        s = f.read()
    except urllib2.HTTPError as e:
        print "HTTP Error "+str(e.code)
        print e.read()
        raise e
    # Parse file object using ElementTree library
    root = ET.fromstring(s)
    # Close URL file object
    f.close()

    d = {}

    print s
    if root.tag == "error":
        raise urllib2.HTTPError

    if operation == "list":
        return [asset.find("aid").text for asset in root]

    return True

##    print root.keys()
##    # Iterate through all the assets in the assetlist
##    for asset in root:
##        print asset
##        # Create dictionary of all the data values in the asset that we care about
##        important_tags = ['tag', 'fleet', 'type', 'subtype', 'gps']
##        asset_d = dict([(k, asset.find(k).text) for k in important_tags])
##        # Add dictionary of asset data values to main dictionary, under the asset number
##        d[asset.attrib['id']] = asset_d
##
##    return d

    ##d = dict([(asset.attrib['id'],
    ##           dict([(k, asset.find(k).text) for k in ['tag', 'fleet', 'type', 'subtype', 'gps']]))
    ##          for asset in xml.etree.ElementTree.parse(urllib2.urlopen(URL)).getroot()])
    ##    
    ##print d


operation = "add"
url = base_url+"&".join(["=".join(x) for x in arguments[operation]])
result = send_omi_call(url.format("1111"), item)
print result

try:
    for item in ["editgps", "edit", "list", "delete"]:
        # Build URL
        url = base_url+"&".join(["=".join(x) for x in arguments[item]])
        # Send URL, if 'delete' then send one for every aid retrieved
        if item == "delete":
           for a in aid_list:
               send_omi_call(url.format(a), item)
        else:
           result = send_omi_call(url, item)
        # If 'list', save list of aids
        if item == "list":
           aid_list = result
           print aid_list
        print ""
        time.sleep(1)
except Exception as e:
   print "Exception when trying to send: {0}".format(url)
   print e
