import glob

out_filename = "Sienna QA Extracts.csv"
files = ['zonarshipmentidboxid_09_19-2014.csv',
         'zonarshipmentidboxid_11-13-2014.csv',
         'zonarshipmentidboxid_11-17-2014.csv',
         'zonarshipmentidboxid_11-21-2014.csv',
         'zonarshipmentidboxid_01-09-2015.csv',
         'zonarshipmentidboxid_01-19-2015.csv',
         'zonarshipmentidboxid_02-17-2015.csv',
         'zonarshipmentidboxid_02-27-2015.csv',
         'zonarshipmentidboxid_03-03-2015.csv',
         'zonarshipmentidboxid_03-25-2015.csv',
         'zonarshipmentidboxid_03-31-2015.csv',
         'zonarshipmentidboxid_04-27-2015.csv',
         'zonarshipmentidboxid_05-19-2015.csv',
         'zonarshipmentidboxid_05-20-2015.csv',
         'zonarshipmentidboxid_05-25-2015.csv',
         'zonarshipmentidboxid_05-29-2015.csv',
         'zonarshipmentidboxid_06-01-2015.csv',
         'zonarshipmentidboxid_06-09-2015.csv',
         'zonarshipmentidboxid_06-15-2015.csv',
         'zonarshipmentidboxid_06-17-2015.csv',
         'zonarshipmentidboxid_06-19-2015.csv',
         'zonarshipmentidboxid_07-13-2015.csv']

with open(out_filename, 'w') as out_file:
    for i, filename in enumerate(files):
        with open(filename) as in_file:
            lines = in_file.readlines()
            if i > 0:
                lines = lines[1:]
            out_file.writelines(lines)