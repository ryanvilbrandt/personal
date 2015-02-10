import re

line_count = 0
last_gpsid = ""
last_date = ""
##filename = 'debug_2014_11_13.txt'
filename = 'debug.txt'

with open(filename) as input_file:
    with open('output.txt', 'a') as output_file:
        for line in input_file:
            # If we have lines to count, count down by one
            if line_count > 0:
                line_count -= 1
                # When we're at zero, grab the appropriate line
                if line_count == 0:
                    output_file.write(
                        "{:<22} {}: {}".format(
                            last_date,
                            last_gpsid,
                            line
                            )
                        )
            else:
                # We want to look for a particular test to start, then look for the line 2 after it
                if "(Check for marked bad NAND blocks)" in line:
                    last_date = line.split('(')[0][19:]
                    line_count = 2
                elif "Attempting to program GPSID:" in line:
                    last_gpsid = line[29:].strip('\n')
