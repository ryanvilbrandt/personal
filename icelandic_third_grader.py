# http://i.imgur.com/zlBQvYF.jpg

def main():
    for a in xrange(100):
        for b in xrange(100):
            if 6*b + 3*a < 30:
                continue
            if 6*b + 3*a > 30:
                break
            for c in xrange(100):
                if 3*a + 3*b + 3*c < 33:
                    continue
                if 3*a + 3*b + 3*c > 33:
                    break
                print a,b,c,(20-(a+b+c))

main()
