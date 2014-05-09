# represent rational numbers as simple continued fractions.
#      1
# a + ------------
#          1
#     b + --------
#               1
#          c + ---
#               d
# is represented as [a, b, c, d].
#
# x/y can be [a] or it can be [a, other terms].
# In both cases, a is floor(x/y).  In the first case,
# x/y == a; in the second case, "other terms" is the continued-fraction 
#	representation of y/(x - ay).
# 
# Only handles positive numbers for now.

import sys

def contfrac_div_wrapper(x,y):
        num, denom = x,y
        while not (int(num) == num and int(denom) == denom):
                num *= 10
                denom *= 10
        return contfrac_div(int(num), int(denom))

def contfrac_div (x, y):
	'''Return the ratio of two positive ints as a continued fraction.'''
	a = x/y
	if a * y == x:
		return [a]
	else:
		list = contfrac_div(y, x - a * y)
		list.insert(0, a)
		return list


# returns (num, denom).

def rationalize_contfrac (frac):
	'''Convert a finite continued fraction to a ratio of two ints.'''
	if len(frac) == 0:
		return (1, 0)
	elif len(frac) == 1:
		return (frac[0], 1)
	else:
		remainder = frac[1:len(frac)]
		# print "calling rationalize_contfrac with " + `remainder`
		(num, denom) = rationalize_contfrac(remainder)
		# fraction is now frac[0] + 1/(num/denom), which is frac[0] +
		# denom/num.
		# print("%s * %s + %s" % (frac[0], num, denom))
		return (frac[0] * num + denom, num)


def test1():
	'''Verify that the basic continued-fraction manipulation stuff works.'''
	testnums = [(1, 1), (7, 3), (5, 15), (15, 11), (19, 15),
                    (-27, 73), (73, 27),
                    (13,33), (7,33), (20,33)]
	for i in testnums:
		(num, denom) = i
		sys.stdout.write( "%d/%d = " % (num, denom))
		contfrac = contfrac_div_wrapper(num, denom)
		sys.stdout.write(`contfrac` + " = ")
		(num, denom) = rationalize_contfrac(contfrac)
		sys.stdout.write("%d/%d\n" % (num, denom))


# do an ASCII graphics rendering, like in the comments at the top of this file.
# 
# The base case: an integer.  (42), for example.  Gets laid out as "42 ".
# The recursive case: (x, ...).  Gets laid out as
#      1
# x + ---
#      (rendering of "...")
#
# We'd like to extend the dashes and perhaps center the 1.  So we have to 
# compute the width of the rendering of "...".  If "..." is an integer, that's
# just the length of "..." plus one.  The width of that ugly thing above is
# the width of x, plus four, plus the width of the rendering of "...".

infinity_string = "infinity "

def rendering_width (frac):
	'''Return the width in chars needed to display a continued fraction.'''
	if len(frac) == 0:
		return len(infinity_string)
	elif len(frac) == 1:
		return 1 + len(`frac[0]`)
	else:
		return (4 + len(`frac[0]`) + 
			rendering_width(frac[1:len(frac)]))


# OK, so to actually lay it out:

def print_contfrac_helper(lmargin, frac):
	'''Print a continued fraction with a specified left margin width.'''
	if len(frac) == 0:
		print " " * lmargin + infinity_string
	elif len(frac) == 1:
		print " " * lmargin + `frac[0]`  + " "
	else:
		numwidth = len(`frac[0]`)
		tailwidth = rendering_width(frac[1:len(frac)])
		centering_width = (tailwidth - 1)/2
		# print "one over"
		print " " * (lmargin + numwidth + 4 + centering_width) + "1"
		# print the line of minuses
		print " " * lmargin + `frac[0]` + " + " + "-" * (tailwidth + 1)
		# print the rest of the expression
		print_contfrac_helper(lmargin + numwidth + 4, 
			frac[1:len(frac)])
		

def print_contfrac(frac):
	'''Print a continued fraction.'''
	print_contfrac_helper(0, frac)


def test2(num, denom):
	'''Print out and convert a single ratio.'''
	frac = contfrac_div_wrapper(num, denom)
	print_contfrac(frac)
	(num, denom) = rationalize_contfrac(frac)
	print "( = %d/%d)" % (num, denom)

test1()
test2(12,33)
