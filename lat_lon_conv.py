a = "001YM003        8511720        2014011721425500012214520000472616"

a = [a[0:3],
     a[3:4],
     a[4:5],
     a[5:8],
     a[8:16],
     a[16:31],
     a[31:39],
     a[39:45],
     a[45:55],
     a[55:]
     ]

##print a

def DmsToDegrees(lat, lon):
    lat_sec = lat%100
    lat_min = (lat/100)%100
    lat_deg = lat/10000
    lat = lat_deg + (lat_min*60 + lat_sec)/3600.0
    
    lon_sec = lon%100
    lon_min = (lon/100)%100
    lon_deg = lon/10000
    lon = lon_deg + (lon_min*60 + lon_sec)/3600.0

    return lat, lon

def SecsToDegrees(lat, lon):
    lat = lat/3600.0
    lon = lon/3600.0
##    if lat > 180: lat -= 360
##    if lon > 180: lon -= 360
    return lat, lon

print DmsToDegrees(805411,285713)
