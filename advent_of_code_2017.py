# http://adventofcode.com/2017/about

from math import ceil

problem_1_input = \
    "892195969991735837915273868729548694237967495115412399373194562526947585337233793568278265279199883197167" + \
    "634791293177986152566236718332617536487236879747167999983363832257912445756887314879229925864477761357139" + \
    "855548522513798899853896612387146687716264599943289416326727256525173953861534244979466587895429399159924" + \
    "916364476319573895566795393368411672387263615582128377676293612892723762237191146714286233543514411813323" + \
    "197995953854871628225358543514157867372265718724276911699514971458844849349726276329135118243155698271218" + \
    "844347387457343656446381799296893222256198484465873714311777937421161581798189554141474236239447612421883" + \
    "232173914183732126332838194648583472419154369952477422666389517569944428464617457124369349242479612422673" + \
    "241361777576466946622932243728551273284837934497511114334421486262244982914734452113946361245377351849815" + \
    "584855691778894798219822463298387771923329337634394654439458564233259451453345316753241438267739439225497" + \
    "515276522424441532462541528195782818326918562247278496495764435386667383577543385186827269732261223156824" + \
    "351164841648424564925198783625721396988984481558391866483955533972212164693898955412719161648411279149413" + \
    "443192896864258215498543827458438871355879336892721675937111952479183496982825163456282747678364612135596" + \
    "373533447719867384667516572262124225585623974278833981365494628646614588114147473559138853453189448624976" + \
    "774641922469183942857695986376428944876851497914443873513862319484181787593572987444669767939526294424531" + \
    "262999564948571142342741129862311311313166798363442745792896227642881893134498151552326647933689596516859" + \
    "342242244584714818773791567187322217164347852843751875979415198165627534263527828414549217234322361937785" + \
    "185174993256753483876378332521824515977173397535784236923629636713469151526399149548322849831431526219478" + \
    "653861754364155275865511643923249858589466142474763778413826829226663398467569555747267195129525138917561" + \
    "785436449855933951538973995881954521124753369223898312843734771532342383282987422334196585128526526324291" + \
    "777689689492346231786335851551413876834969878"

def problem_1_a():
    def parse_digits(digits):
        """
        :param digits: str of digits
        :return:
        """
        total = 0
        for i, c in enumerate(digits):
            if int(digits[i]) == int(digits[(i + 1) % len(digits)]):
                total += int(c)
        return total

    print("1122", parse_digits("1122"))
    print("1111", parse_digits("1111"))
    print("1234", parse_digits("1234"))
    print("91212129", parse_digits("91212129"))
    print(parse_digits(problem_1_input))

def problem_1_b():
    def parse_digits(digits):
        """
        :param digits: str of digits
        :return:
        """
        total = 0
        len_digits = len(digits)
        for i, c in enumerate(digits):
            a = int(digits[i])
            b = int(digits[(i + len_digits // 2) % len_digits])
            if a == b:
                total += int(c)
        return total

    for digits in ["1212", "1221", "123425", "123123", "12131415", problem_1_input]:
        print(digits, parse_digits(digits))

        
puzzle_2_input = """
737	1866	1565	1452	1908	1874	232	1928	201	241	922	281	1651	1740	1012	1001
339	581	41	127	331	133	51	131	129	95	499	527	518	435	508	494
1014	575	1166	259	152	631	1152	1010	182	943	163	158	1037	1108	1092	887
56	491	409	1263	1535	41	1431	1207	1393	700	1133	53	131	466	202	62
632	403	118	352	253	672	711	135	116	665	724	780	159	133	90	100
1580	85	1786	1613	1479	100	94	1856	546	76	1687	1769	1284	1422	1909	1548
479	356	122	372	786	1853	979	116	530	123	1751	887	109	1997	160	1960
446	771	72	728	109	369	300	746	86	910	566	792	616	84	338	57
6599	2182	200	2097	4146	7155	7018	1815	1173	4695	201	7808	242	3627	222	7266
1729	600	651	165	1780	2160	626	1215	149	179	1937	1423	156	129	634	458
1378	121	146	437	1925	2692	130	557	2374	2538	2920	2791	156	317	139	541
1631	176	1947	259	2014	153	268	752	2255	347	227	2270	2278	544	2379	349
184	314	178	242	145	410	257	342	183	106	302	320	288	151	449	127
175	5396	1852	4565	4775	665	4227	171	4887	181	2098	4408	2211	3884	2482	158
1717	3629	244	258	281	3635	235	4148	3723	4272	3589	4557	4334	4145	3117	4510
55	258	363	116	319	49	212	44	303	349	327	330	316	297	313	67
"""

def problem_2_a():
    def calculate_checksum(text):
        checksum = 0
        for row in text.strip('\n').split('\n'):
            sorted_values = sorted([int(c) for c in row.split('\t')])
            chk = max(sorted_values) - min(sorted_values)
            checksum += chk
            print(chk)
        return checksum
    a = """
5	1	9	5
7	5	3
2	4	6	8
"""
    print("Checksum:", calculate_checksum(a))
    print("Checksum:", calculate_checksum(puzzle_2_input))
    
def problem_2_b():
    def calculate_checksum(text):
        checksum = 0
        for row in text.strip('\n').split('\n'):
            int_values = [int(c) for c in row.split('\t')]
            for i, x in enumerate(int_values):
                for j, y in enumerate(int_values):
                    if (x != y) and (x % y == 0):
                        chk = int(x / y)
                        print(chk)
                        checksum += chk
        return checksum
    a = """
5	9	2	8
9	4	7	3
3	8	6	5
"""
    print("Checksum:", calculate_checksum(a))
    print("Checksum:", calculate_checksum(puzzle_2_input))


def problem_3_a():
    def build_grid(target_num, stop_at_num=True):
        array_size = ceil(target_num ** 0.5)
        if array_size % 2 == 0:
            array_size += 1
        
        a = []
        for i in range(array_size):
            a.append([" "]*array_size)
        
        center = int((array_size) / 2)
        a[center][center] = 1
        count = 2
        for i in range(2, target_num):
            layer = i
            length = layer * 2 - 1
            start_x = center + layer - 1
            start_y = center + max(0, layer - 2)
            x = start_x
            y = start_y
            for j in range(length - 1):
                a[y - j][x] = count
                if count >= target_num and stop_at_num:
                    return a, x - center, (y - j) - center
                count += 1
            y -= length-2
            for j in range(1, length):
                a[y][x - j] = count
                if count >= target_num and stop_at_num:
                    return a, (x - j) - center, y - center
                count += 1
            x -= length-1
            for j in range(1, length):
                a[y + j][x] = count
                if count >= target_num and stop_at_num:
                    return a, x - center, (y + j) - center
                count += 1
            y += length - 1
            for j in range(1, length):
                a[y][x + j] = count
                if count >= target_num and stop_at_num:
                    return a, (x + j) - center, y - center
                count += 1
            x += length - 1
            
            if count > target_num:
                break
        
        return a, 0, 0
              
    g, x, y = build_grid(265149)
    # for line in g:
        # print("|" + "|".join(["{0:>3}".format(c) for c in line]) + "|")
    print([x, y])
    print(abs(x) + abs(y))

def problem_3_b():
    def print_grid(g):
        for line in g:
            print("|" + "|".join(["{0:>6}".format(c) for c in line]) + "|")

    def get_value(grid, x, y):
        def read_cell(grid, x, y):
            if x < 0 or y < 0:
                return 0
            try:
                x = grid[y][x]
            except IndexError:
                return 0
            if x == " ":
                return 0
            return x
            
        total = 0
        total += read_cell(grid, x - 1, y - 1)
        total += read_cell(grid, x - 1, y)
        total += read_cell(grid, x - 1, y + 1)
        total += read_cell(grid, x, y - 1)
        total += read_cell(grid, x, y + 1)
        total += read_cell(grid, x + 1, y - 1)
        total += read_cell(grid, x + 1, y)
        total += read_cell(grid, x + 1, y + 1)
        return total

    def build_grid(target_num, stop_at_num=True):
        array_size = ceil(target_num ** 0.5)
        if array_size % 2 == 0:
            array_size += 1
        
        a = []
        for i in range(array_size):
            a.append([" "]*array_size)
        
        center = int((array_size) / 2)
        a[center][center] = 1
        count = 2
        for i in range(2, target_num):
            layer = i
            length = layer * 2 - 1
            x = center + layer - 1
            y = center + max(0, layer - 2)
            for j in range(length - 1):
                total = get_value(a, x, y - j)
                a[y - j][x] = total
                if count >= target_num and stop_at_num:
                    return a, x - center, (y - j) - center
                count += 1
            y -= length-2
            for j in range(1, length):
                total = get_value(a, x - j, y)
                a[y][x - j] = total
                if count >= target_num and stop_at_num:
                    return a, (x - j) - center, y - center
                count += 1
            x -= length-1
            for j in range(1, length):
                total = get_value(a, x, y + j)
                a[y + j][x] = total
                if count >= target_num and stop_at_num:
                    return a, x - center, (y + j) - center
                count += 1
            y += length - 1
            for j in range(1, length):
                total = get_value(a, x + j, y)
                a[y][x + j] = total
                if count >= target_num and stop_at_num:
                    return a, (x + j) - center, y - center
                count += 1
            x += length - 1
            
            if count > target_num:
                break
        
        return a, 0, 0
              
    g, x, y = build_grid(81)
    print_grid(g)
    print([x, y])
    print(abs(x) + abs(y))
    
    
def problem_4_a():
    def check_valid_passphrase(passphrase):
        passphrase_list = passphrase.split(' ')
        # print(passphrase_list)
        # print(list(set(passphrase_list)))
        return len(set(passphrase_list)) == len(passphrase_list)
    
    def find_valid_passphrases(passphrases):
        passphrases = passphrases.split('\n')
        return len([p for p in passphrases if check_valid_passphrase(p)])
        
    print(check_valid_passphrase("aa bb cc dd ee"))
    print(check_valid_passphrase("aa bb cc dd aa"))
    print(check_valid_passphrase("aa bb cc dd aaa"))
    with open("D:\\GitHub_ryanvilbrandt\\personal\\inputs\\advent_of_code_2017_problem_4_input.txt") as f:
        problem_4_input = f.read()
    print(find_valid_passphrases(problem_4_input))
    
def problem_4_b():
    def check_valid_passphrase(passphrase):
        passphrase_list = ["".join(sorted(p)) for p in passphrase.split(' ')]
        # print(passphrase_list)
        # print(list(set(passphrase_list)))
        return len(set(passphrase_list)) == len(passphrase_list)
    
    def find_valid_passphrases(passphrases):
        passphrases = passphrases.split('\n')
        return len([p for p in passphrases if check_valid_passphrase(p)])
        
    print(check_valid_passphrase("abcde fghij"))
    print(check_valid_passphrase("abcde xyz ecdab"))
    print(check_valid_passphrase("a ab abc abd abf abj"))
    print(check_valid_passphrase("iiii oiii ooii oooi oooo"))
    print(check_valid_passphrase("oiii ioii iioi iiio"))
    with open("D:\\GitHub_ryanvilbrandt\\personal\\inputs\\advent_of_code_2017_problem_4_input.txt") as f:
        problem_4_input = f.read()
    print(find_valid_passphrases(problem_4_input))


def problem_5_a():
    def jump(jump_list):
        index = 0
        jump_count = 0
        while 0 <= index < len(jump_list):
            # print(jump_list)
            last_index = index
            index += jump_list[index]
            jump_list[last_index] += 1
            jump_count += 1
        # print(jump_list)
        # print()
        return jump_count
    a = [0, 3, 0, 1, -3]
    print(a, jump(a[:]))
    with open("D:\\GitHub_ryanvilbrandt\\personal\\inputs\\advent_of_code_2017_problem_5_input.txt") as f:
        input_list = f.read().strip('\n').split('\n')
    input_list = [int(x) for x in input_list]
    print(jump(input_list))

def problem_5_b():
    def jump(jump_list):
        index = 0
        jump_count = 0
        while 0 <= index < len(jump_list):
            # print(jump_list)
            last_index = index
            index += jump_list[index]
            jump_list[last_index] += 1 if jump_list[last_index] < 3 else -1
            jump_count += 1
        # print(jump_list)
        # print()
        return jump_count
    a = [0, 3, 0, 1, -3]
    print(a, jump(a[:]))
    with open("D:\\GitHub_ryanvilbrandt\\personal\\inputs\\advent_of_code_2017_problem_5_input.txt") as f:
        input_list = f.read().strip('\n').split('\n')
    input_list = [int(x) for x in input_list]
    print(jump(input_list))


def problem_6_a():
    def check_history(history, new_list):
        if new_list in history:
            return False
        history.append(new_list[:])
        return True
    def reallocate(blocks):
        history = []
        loops = 0
        while check_history(history, blocks):
            max_index = blocks.index(max(blocks))
            blocks_to_redistribute = blocks[max_index]
            blocks[max_index] = 0
            for i in range(blocks_to_redistribute):
                blocks[(max_index + i + 1) % len(blocks)] += 1
            # print(history, blocks)
            loops += 1
        return loops
    print(reallocate([0, 2, 7, 0]))
    print(reallocate([4, 1, 15, 12, 0, 9, 9, 5, 5, 8, 7, 3, 14, 5, 12, 3]))

def problem_6_b():
    def check_history(history, new_list):
        if history.count(new_list) == 2:
            return False
        history.append(new_list[:])
        return True
    def reallocate(blocks):
        history = []
        loops = 0
        while check_history(history, blocks):
            max_index = blocks.index(max(blocks))
            blocks_to_redistribute = blocks[max_index]
            blocks[max_index] = 0
            for i in range(blocks_to_redistribute):
                blocks[(max_index + i + 1) % len(blocks)] += 1
            # print(history, blocks)
            loops += 1
        return loops
    print(reallocate([0, 2, 7, 0]))
    print(reallocate([4, 1, 15, 12, 0, 9, 9, 5, 5, 8, 7, 3, 14, 5, 12, 3]))
            


