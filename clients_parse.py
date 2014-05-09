import re, pyperclip

clients = """ ID     | MAC               | IP              | Version        | Last TS             | Session
--------+-------------------+-----------------+----------------+---------------------+-----------------------
      3 | 64:fc:8c:00:01:c2 |  10.182.137.168 |      0.6.630.0 | 2011-04-28 12:59:02 | PumpControllerProtocol
      7 | 64:fc:8c:00:01:2f |  10.182.137.173 |      0.6.630.0 | 2011-04-28 12:41:24 | PumpControllerProtocol
     13 | 64:fc:8c:00:01:84 |  10.182.137.169 |      0.6.630.0 | 2011-04-28 13:06:16 | PumpControllerProtocol
     15 | 64:fc:8c:10:00:12 |  10.181.152.170 |      0.6.630.0 | 2011-04-28 12:58:20 | PumpControllerProtocol
     25 | 64:fc:8c:00:00:36 |  10.181.146.168 |      0.6.630.0 | 2011-04-28 13:07:44 | PumpControllerProtocol
     31 | 64:fc:8c:00:00:35 |  10.181.146.167 |      0.6.630.0 | 2011-04-28 12:58:36 | PumpControllerProtocol
     33 | 64:fc:8c:00:01:a2 |  10.182.137.170 |      0.6.630.0 | 2011-04-28 13:01:42 | PumpControllerProtocol
     35 | 64:fc:8c:00:00:38 |  10.181.146.170 |      0.6.630.0 | 2011-04-28 13:07:42 | PumpControllerProtocol
     46 |                   |                 |                | 2011-04-28 13:06:34 | PumpControllerProtocol
     52 | 64:fc:8c:00:00:37 |  10.181.146.169 |      0.6.630.0 | 2011-04-28 13:05:46 | PumpControllerProtocol
     64 | 64:fc:8c:00:00:1d |  10.181.152.172 |      0.6.630.0 | 2011-04-28 13:02:30 | PumpControllerProtocol
     65 | 64:fc:8c:00:00:84 |   10.181.15.172 |   1536.0.29.30 | 2011-04-28 13:05:19 | PumpControllerProtocol
     71 | 64:fc:8c:00:00:90 |   10.181.15.173 |   1536.0.29.30 | 2011-04-28 13:07:17 | PumpControllerProtocol
     73 | 64:fc:8c:00:00:7f |   10.181.15.171 |   1536.0.29.30 | 2011-04-28 13:07:37 | PumpControllerProtocol
     74 | 64:fc:8c:00:00:89 |   10.181.15.170 |   1536.0.29.30 | 2011-04-28 13:06:48 | PumpControllerProtocol
     76 | 64:fc:8c:00:00:9a |   10.181.15.169 |   1536.0.29.30 | 2011-04-28 13:07:56 | PumpControllerProtocol
     77 | 64:fc:8c:00:00:92 |   10.181.15.168 |   1536.0.29.30 | 2011-04-28 13:07:37 | PumpControllerProtocol
     78 | 64:fc:8c:00:00:9b |   10.181.15.167 |   1536.0.29.30 | 2011-04-28 13:07:45 | PumpControllerProtocol
     82 |                   |                 |                | 2011-04-28 13:08:05 | SSHClientProtocol
    104 | 64:fc:8c:00:01:cb |  10.161.147.169 |      0.6.630.0 | 2011-04-28 13:00:51 | PumpControllerProtocol
    107 | 64:fc:8c:00:01:96 |  10.161.147.167 |      0.6.630.0 | 2011-04-28 12:55:10 | PumpControllerProtocol
    109 | 64:fc:8c:00:00:ea |  10.182.137.171 |      0.6.630.0 | 2011-04-28 12:59:20 | PumpControllerProtocol
    147 | 64:fc:8c:00:01:de |  10.161.146.172 |      0.6.630.0 | 2011-04-28 13:03:12 | PumpControllerProtocol
    150 | 64:fc:8c:00:01:e1 |  10.161.146.171 |      0.6.630.0 | 2011-04-28 12:42:17 | PumpControllerProtocol
    153 | 64:fc:8c:00:01:dc |  10.161.146.170 |      0.6.630.0 | 2011-04-28 12:59:38 | PumpControllerProtocol
    154 | 64:fc:8c:00:01:9e |  10.161.146.174 |      0.6.630.0 | 2011-04-28 13:07:33 | PumpControllerProtocol
    172 |                   |                 |                | 2011-04-27 16:28:15 | SSHClientProtocol
    182 | 64:fc:8c:00:01:e3 |  10.161.172.167 |      0.6.630.0 | 2011-04-28 13:08:05 | PumpControllerProtocol
    185 | 64:fc:8c:00:00:db |  10.161.172.168 |      0.6.630.0 | 2011-04-28 13:07:56 | PumpControllerProtocol
    186 | 64:fc:8c:00:01:68 |  10.161.172.170 |      0.6.630.0 | 2011-04-28 13:07:33 | PumpControllerProtocol
    187 | 64:fc:8c:00:01:6c |  10.161.172.171 |      0.6.630.0 | 2011-04-28 13:08:01 | PumpControllerProtocol
    188 | 64:fc:8c:00:01:c3 |  10.161.172.169 |      0.6.630.0 | 2011-04-28 13:04:10 | PumpControllerProtocol
    196 | 64:fc:8c:00:01:87 |  10.161.146.168 |      0.6.630.0 | 2011-04-28 13:01:13 | PumpControllerProtocol
    270 | 64:fc:8c:00:00:a1 |  10.181.219.168 |      0.6.621.0 | 2011-04-28 12:52:13 | PumpControllerProtocol
    273 | 64:fc:8c:00:00:7a |  10.181.219.171 |      0.6.621.0 | 2011-04-28 12:53:01 | PumpControllerProtocol
    283 | 64:fc:8c:00:00:7c |  10.181.219.167 |      0.6.621.0 | 2011-04-28 13:04:21 | PumpControllerProtocol
    284 | 64:fc:8c:00:01:9b |  10.182.137.172 |      0.6.630.0 | 2011-04-28 13:05:39 | PumpControllerProtocol
    289 | 64:fc:8c:00:01:a8 |  10.161.146.167 |      0.6.630.0 | 2011-04-28 13:06:40 | PumpControllerProtocol
    313 | 64:fc:8c:00:00:e4 |   10.181.95.168 |      0.6.630.0 | 2011-04-28 12:08:45 | PumpControllerProtocol
    326 | 64:fc:8c:10:00:17 |  10.181.152.173 |      0.6.630.0 | 2011-04-28 12:59:19 | PumpControllerProtocol
    333 | 64:fc:8c:00:00:d8 |  10.182.137.167 |      0.6.630.0 | 2011-04-28 13:02:41 | PumpControllerProtocol
    336 | 64:fc:8c:10:00:18 |  10.181.152.174 |      0.6.630.0 | 2011-04-28 12:54:52 | PumpControllerProtocol
    343 | 64:fc:8c:00:01:d4 |  10.161.146.169 |      0.6.630.0 | 2011-04-28 13:06:20 | PumpControllerProtocol
    344 | 64:fc:8c:00:01:3b |  10.161.146.173 |      0.6.630.0 | 2011-04-28 12:57:14 | PumpControllerProtocol
    350 | 64:fc:8c:00:00:57 |  10.181.152.171 |      0.6.630.0 | 2011-04-28 13:05:23 | PumpControllerProtocol
    352 | 64:fc:8c:00:00:d4 |  10.161.147.173 |      0.6.630.0 | 2011-04-28 12:57:32 | PumpControllerProtocol
    404 | 64:fc:8c:00:01:cc |  10.161.147.170 |      0.6.630.0 | 2011-04-28 13:02:45 | PumpControllerProtocol
    405 | 64:fc:8c:00:01:bc |  10.161.147.172 |      0.6.630.0 | 2011-04-28 13:01:11 | PumpControllerProtocol
    408 | 64:fc:8c:00:00:f3 |  10.161.144.169 |      0.6.630.0 | 2011-04-28 12:02:40 | PumpControllerProtocol
    409 | 64:fc:8c:00:01:49 |  10.161.144.170 |      0.6.630.0 | 2011-04-28 12:59:45 | PumpControllerProtocol
    411 | 64:fc:8c:00:01:25 |  10.161.144.168 |      0.6.630.0 | 2011-04-28 13:05:20 | PumpControllerProtocol
    412 | 64:fc:8c:00:01:06 |  10.161.144.167 |      0.6.630.0 | 2011-04-28 12:57:13 | PumpControllerProtocol
    413 | 64:fc:8c:00:01:8e |  10.161.144.172 |      0.6.630.0 | 2011-04-28 13:01:30 | PumpControllerProtocol
    415 | 64:fc:8c:00:00:75 |  10.161.113.168 |      0.6.621.0 | 2011-04-28 13:07:42 | PumpControllerProtocol
    416 | 64:fc:8c:00:00:34 |  10.161.113.173 |      0.6.621.0 | 2011-04-28 13:08:01 | PumpControllerProtocol
    417 | 64:fc:8c:00:00:77 |  10.161.113.167 |      0.6.621.0 | 2011-04-28 13:07:46 | PumpControllerProtocol
    418 | 64:fc:8c:00:00:9f |  10.161.113.170 |      0.6.621.0 | 2011-04-28 13:03:36 | PumpControllerProtocol
    419 | 64:fc:8c:00:00:9c |  10.161.113.171 |      0.6.621.0 | 2011-04-28 13:03:27 | PumpControllerProtocol
    420 | 64:fc:8c:00:00:33 |  10.161.113.172 |      0.6.621.0 | 2011-04-28 13:06:06 | PumpControllerProtocol
    421 | 64:fc:8c:00:00:78 |  10.161.113.169 |      0.6.621.0 | 2011-04-28 13:07:40 | PumpControllerProtocol
    422 | 64:fc:8c:00:00:86 |  10.161.113.176 |      0.6.621.0 | 2011-04-28 13:07:34 | PumpControllerProtocol
    424 | 64:fc:8c:00:00:70 |  10.161.113.175 |      0.6.621.0 | 2011-04-28 13:07:50 | PumpControllerProtocol
    425 | 64:fc:8c:00:00:f0 |   10.181.95.169 |      0.6.630.0 | 2011-04-28 12:03:05 | PumpControllerProtocol
    427 | 64:fc:8c:00:00:fe |  10.161.147.171 |      0.6.630.0 | 2011-04-28 12:58:22 | PumpControllerProtocol
    431 | 64:fc:8c:00:00:a5 |  10.181.219.173 |      0.6.621.0 | 2011-04-28 11:57:20 | PumpControllerProtocol
    433 | 64:fc:8c:00:00:e2 |  10.161.144.171 |      0.6.630.0 | 2011-04-28 13:08:04 | PumpControllerProtocol
    434 | 64:fc:8c:00:01:7c |  10.161.147.174 |      0.6.630.0 | 2011-04-28 13:02:54 | PumpControllerProtocol
    435 |                   |                 |                |                None | PumpControllerProtocol
    436 | 64:fc:8c:00:00:99 |  10.161.113.174 |      0.6.621.0 | 2011-04-28 13:07:28 | PumpControllerProtocol
    437 | 64:fc:8c:00:01:b8 |  10.161.144.173 |      0.6.630.0 | 2011-04-28 12:16:39 | PumpControllerProtocol
    438 | 64:fc:8c:00:01:b8 |  10.161.144.173 |      0.6.630.0 | 2011-04-28 13:07:15 | PumpControllerProtocol
    439 | 64:fc:8c:00:01:91 |   10.181.95.172 |      0.6.630.0 | 2011-04-28 13:02:02 | PumpControllerProtocol
    440 | 64:fc:8c:00:00:7b |  10.181.219.172 |      0.6.621.0 | 2011-04-28 12:27:24 | PumpControllerProtocol
    441 | 64:fc:8c:00:00:7d |  10.181.219.169 |      0.6.582.0 | 2011-04-28 12:27:24 | PumpControllerProtocol
    442 | 64:fc:8c:00:00:a3 |  10.181.219.170 |      0.6.621.0 | 2011-04-28 12:27:24 | PumpControllerProtocol
    444 | 64:fc:8c:00:01:cf |   10.181.95.167 |      0.6.630.0 | 2011-04-28 12:56:53 | PumpControllerProtocol
    445 | 64:fc:8c:00:01:b3 |   10.181.95.171 |      0.6.630.0 | 2011-04-28 13:04:35 | PumpControllerProtocol
    446 | 64:fc:8c:00:01:ba |   10.181.95.173 |      0.6.630.0 | 2011-04-28 13:06:58 | PumpControllerProtocol
    448 | 64:fc:8c:00:00:ef |   10.181.95.170 |      0.6.612.0 | 2011-04-28 12:41:20 | PumpControllerProtocol
    449 | 64:fc:8c:00:00:30 |      10.0.2.200 |      0.6.630.0 | 2011-04-28 12:50:22 | PumpControllerProtocol
    450 | 64:fc:8c:00:00:e4 |   10.181.95.168 |      0.6.630.0 | 2011-04-28 12:52:53 | PumpControllerProtocol
    451 | 64:fc:8c:00:00:e4 |   10.181.95.168 |      0.6.630.0 | 2011-04-28 13:04:55 | PumpControllerProtocol
    452 | 64:fc:8c:00:00:30 |      10.0.2.200 |      0.6.630.0 | 2011-04-28 12:59:11 | PumpControllerProtocol
    453 | 64:fc:8c:00:00:39 |  10.181.146.171 |      0.6.630.0 | 2011-04-28 12:56:41 | PumpControllerProtocol
    454 | 64:fc:8c:00:01:99 |  10.161.144.174 |      0.6.630.0 | 2011-04-28 13:06:59 | PumpControllerProtocol
    455 | 64:fc:8c:00:01:df |   10.181.95.169 |      0.6.612.0 | 2011-04-28 13:07:54 | PumpControllerProtocol
    456 | 64:fc:8c:00:01:db |   10.181.95.170 |      0.6.612.0 | 2011-04-28 13:07:56 | PumpControllerProtocol"""

##c = pyperclip.getcb()
##if c.startswith('Clients'):
##    clients = c

## 145 10.181.146. Springdale
## 151 10.181.152. Tumwater
## 219 10.181.219. Knoxville 
## 232             Ontario 
## 294 10.181.95.  MSC 
## 341 10.181.15.  N. Las Vegas 
## 350             Mountain Home
## 437 10.182.137. ???
## 638             Caldwell 
## 640             Jerome Twin Falls 
## 713 10.161.113. Latta 
## 744 10.161.144. Ogden 
## 746 10.161.146. Salt Lake City 
## 747 10.161.147. Springville 
## 772 10.161.172. North Salt Lake 
## 773             Nephi 
## 774             Snowville 
## 775             St. George 
## 777             Boise

ip = r"10.181.95.(\d+)"
##ip = "None"
fw = r"0.6.630.0"

temp = [line for line in clients.split('\n')
        if re.search(ip,line)]
for line in temp:
    print line
print ""
temp = [line for line in temp
        if not re.search(fw,line)]
fw_list = fw.split('.')
for line in temp:
    n = line.split('|')[0].strip()
    print "installfw {0} {1} Z{2}{3}r{4}.bin".format(n,fw,fw_list[0],
                                                     fw_list[1],fw_list[2])


