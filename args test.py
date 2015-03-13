def print_test(*args):
    return ",".join([str(a) for a in args])

print repr(print_test('a'))
print repr(print_test(1,2,3,4))

try:
    raise ValueError("Test")
except Exception as e:
    print e
