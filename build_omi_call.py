r = raw_input("Paste in JSON string for OMI call: ")
if not r:
  print "No data. Exitting"
else:
  # Split JSON string into tuples, to preserve order
  a = [x.split(":") for x in r.strip("{}").split(',')]
  # Convert tuples to string of format <key>=<value>, and join around &
  # This will be the PHP argument string
  new_list = []
  for x in a:
    if len(x) != 2:
      print "Invalid value in string: {0}"
      break
    new_list.append("{0}={1}".format(x[0].strip('"'),x[1].strip('"').replace(' ',"%20")))
  else:
    a = "&".join(a)
    # Append web address and print
    print "https://qa1.zonarsystems.net/interface.php?"+a
