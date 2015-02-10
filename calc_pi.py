i = 1.0
a = 0.0
positive = True
iters = 10000000
print_point = 100001

while True:
    if positive:
        a += 1/i
    else:
        a += -1/i
    i += 2
    positive = not positive
    if i % print_point == 0:
        print a*4
