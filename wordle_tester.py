from collections import defaultdict

from wordle_solver import check_status, get_word_list, get_possible_words


def get_next_pattern():
    status_list = ["n", "m", "y"]
    for a in status_list:
        for b in status_list:
            for c in status_list:
                for d in status_list:
                    for e in status_list:
                        if a + b + c + d + e != "yyyyy":
                            yield a + b + c + d + e


def main():
    word_list = get_word_list()
    word_rankings = defaultdict(int)
    for word in ["sores", "cares", "oases", "ourie", "adieu"]:
        print(word)
        for pattern in get_next_pattern():
            c, e, i, w = check_status(pattern, word, defaultdict(list))
            possible_words = get_possible_words(word_list, c, i, e, w)
            word_rankings[word] += len(possible_words)
    print(word_rankings)


if __name__ == "__main__":
    main()
