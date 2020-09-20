import time

elements = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K',
            'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb',
            'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs',
            'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta',
            'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa',
            'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt']

dictionary_path = "inputs/words_alpha.txt"  # new-line delimited list of words
found_words_filepath = "outputs/periodic_words.txt"

def parse_word(letters, remaining_word, word_so_far):
    global elements_lower, found_words
    if letters not in elements_lower:
        return
    word_so_far += letters.title()
    if remaining_word == "":
        found_words.append(word_so_far)
    parse_word(remaining_word[:1], remaining_word[1:], word_so_far)
    if len(remaining_word) > 1:
        parse_word(remaining_word[:2], remaining_word[2:], word_so_far)

def main():
    global elements_lower, found_words
    elements_lower = [e.lower() for e in elements]
    found_words = []

    with open(dictionary_path) as f:
        t1 = time.time()
        for word in f:
            word = word.strip('\n').lower()
            parse_word(word[:1], word[1:], "")
            if len(word) > 1:
                parse_word(word[:2], word[2:], "")
        t2 = time.time()
        print(t2-t1)

    with open(found_words_filepath, 'w') as f:
        f.write("\n".join(found_words))


if __name__ == "__main__":
    main()

    full_dict_count = 0
    with open(dictionary_path) as f:
        for word in f:
            full_dict_count += 1
    parsed_dict_count = 0
    with open(found_words_filepath) as f:
        for word in f:
            parsed_dict_count += 1

    print(full_dict_count)
    print(parsed_dict_count)
    print(parsed_dict_count / float(full_dict_count))