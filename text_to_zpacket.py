in_str = "02 03 0B 00 1D 06 04 00 FD F9 03"  # GetStatusInfo
filename = "blah.txt"

print "Input:",in_str

# Convert string from readable hex to ASCII characters
try:
    a = ''.join([chr(int(x,16)) for x in in_str.split(' ')])
except Exception:
    print "Bad input string"
    raise

print "Writing output to file:",repr(a)

# Write string to file
try:
    with open(filename, 'w') as f:
        f.write(a)
except Exception:
    print "Error when writing to file"
    raise
              

