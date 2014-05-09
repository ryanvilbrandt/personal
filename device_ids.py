import subprocess

start = input("Which serial number are you starting at? ")
num = input("How many serial numbers do you need? ")

i = start
out = ""
while(num > 0):
    if num == 0xFFFFFFFF:
        print "Ran out of serial numbers\n"
        out += "Ran out of serial numbers\n"
        break
    if not (i % 0x100 == 0x00 or i % 0x100 == 0xFF):
        print i
        out += str(i)+"\n"
        num -= 1
    i += 1

filename = 'device_ids {0}-to-{1}.txt'.format(start, i-1)
with open(filename, 'w') as f:
    f.write(out)
print "Device ID list written to "+filename
##os.system('notepad.exe '+filename)
subprocess.Popen('notepad.exe '+filename)
