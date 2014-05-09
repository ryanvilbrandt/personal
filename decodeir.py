import struct, time, gc

# Disable garbage collection, for the sake of verifying processing speeds
gc.disable()

a = 'UYUVUe\xa6eUjUUUU'

def DecodeIR(ir):
    if (len(ir) % 2):
        return len(ir), len(ir) % 2

    out = 0
    for i in range(0,len(ir)/2):
        n = struct.unpack(">H",ir[i*2]+ir[i*2+1])[0]
        temp = ("{0:016b}".format(n))[::2]
        out += int("".join(temp),2) << (i*8)
##        temp = 0
##        for j in range(8):
##            temp |= ((n & (0x02 << (j*2))) >> (j+1))
##        out |= temp << (i << 3)
    return out

t = time.clock()
for i in range(10000):
    print DecodeIR(a[6:])
print (time.clock()-t)/10000

##import timeit
##
##print timeit.timeit('out = 0xF0|0x0F')
##print timeit.timeit('out = 0xF0+0x0F')
