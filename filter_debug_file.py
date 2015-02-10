keep_list = ["GPSID: ",
             "Marked bad blocks: ",
             "Invalid blocks: ",
             "Summary: ",
             "'nand bad "]
replace_dict = {'Cycle count:': '\n'+'='*80+'\n\n'}

with open('debug.txt') as in_file:
    with open('output.txt', 'w') as out_file:
        for line in in_file:
            for item in keep_list:
                if line.startswith(item):
                    out_file.write(line)
                    break
            else:
                for key in replace_dict:
                    if line.startswith(key):
                        out_file.write(replace_dict[key])
                        break
