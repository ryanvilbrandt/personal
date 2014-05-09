try:
    f_in = open("ponies.pon", "r")
except Exception as e:
    print e
else:

    try:
        f_out = open("ponies_parsed.txt", "w")
    except Exception as e:
        print e
    else:

        for line in f_in:
            temp = line.strip('\n').split('`')
            f_out.write("{0} - {1} - {2}\n".format(temp[0], temp[1], temp[2]))

        f_out.close()
    f_in.close()
