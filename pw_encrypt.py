pw = 'pumpapp.zonarsystems.net'
key = 0x7B

def eord(i, k, d=True):
    o = ""
    l = k
    for c in i:
        n = ord(c) ^ l
        o += chr(n)
        l = (d and n) or (not d and ord(c))
    return o

a = eord(pw, key, False)
print repr(a)
print repr(eord(a, 0x7B))

k = 0x7B
print eord('\x0b\x05\x18\x1d\x11\x11\x00^T\x15\x01\x0f\x13\x01\n\n\x07\x11\x08\x1e]@\x0b\x11',k)
print 2112
print eord('\x0b\x05\x18\x1d\x11\x11\x00',k)
print eord('\x0b\x05\x18\x1d\x19\x1d\x01\x05D\x01\x14',k)
