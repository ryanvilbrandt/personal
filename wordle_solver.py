# https://www.powerlanguage.co.uk/wordle/
import random
from collections import defaultdict
from copy import deepcopy
from json import load
from math import inf
from typing import List, Set, Dict


class Strategy:
    @classmethod
    def get_ranked_word_dict(cls, word_list: List[str]):
        raise NotImplementedError

    @classmethod
    def get_suggested_word_highest(cls, possible_words: List[str]) -> str:
        highest_word_ranking = -inf
        highest_word_list = []
        ranked_word_dict = cls.get_ranked_word_dict(possible_words)
        for word, ranking in ranked_word_dict.items():
            if ranking < highest_word_ranking:
                continue
            elif ranking == highest_word_ranking:
                highest_word_list.append(word)
                print(highest_word_ranking, highest_word_list)
            else:
                highest_word_ranking = ranking
                highest_word_list = [word]
                print(highest_word_ranking, highest_word_list)
        return random.choice(highest_word_list)

    @classmethod
    def get_suggested_word_lowest(cls, possible_words: List[str]) -> str:
        lowest_word_ranking = inf
        lowest_word_list = []
        ranked_word_dict = cls.get_ranked_word_dict(possible_words)
        for word, ranking in ranked_word_dict.items():
            if ranking > lowest_word_ranking:
                continue
            elif ranking == lowest_word_ranking:
                lowest_word_list.append(word)
                print(lowest_word_ranking, lowest_word_list)
            else:
                lowest_word_ranking = ranking
                lowest_word_list = [word]
                print(lowest_word_ranking, lowest_word_list)
        return random.choice(lowest_word_list)


class MostCommonLettersStrategy(Strategy):
    multiple_letter_penalty = 2.5

    @classmethod
    def get_ranked_word_dict(cls, word_list: List[str]):
        letter_counts = defaultdict(int)
        for word in word_list:
            for c in word:
                letter_counts[c] += 1
        print(sorted(letter_counts.items(), key=lambda x: x[1], reverse=True))
        ranked_letter_dict = {
            c[0]: i + 1 for i, c in
            enumerate(sorted(letter_counts.items(), key=lambda x: x[1], reverse=True))
        }
        ranked_word_dict = {}
        for word in word_list:
            word_ranking = 0
            for c in word:
                # Prioritize words with more common letters, and non-repeated letters
                # Each word gets a score that's a sum of the ranking of its letters, with each letter's
                # ranking penalized if it occurs more than once in the word
                # E.g. racer = 5*4 + 3*1 + 12*1 + 2*1 + 5*4
                word_ranking += ranked_letter_dict[c] * (((word.count(c) - 1) * cls.multiple_letter_penalty) + 1)
            ranked_word_dict[word] = word_ranking
        return ranked_word_dict

    @classmethod
    def get_suggested_word(cls, possible_words: List[str]) -> str:
        return cls.get_suggested_word_highest(possible_words)


class MostCommonPositionsStrategy(Strategy):
    allow_duplicates = False

    @classmethod
    def get_ranked_word_dict(cls, word_list: List[str]) -> Dict[str, int]:
        word_length = len(word_list[0])
        letter_position_counts = defaultdict(lambda: [0] * word_length)
        for word in word_list:
            for i, c in enumerate(word):
                letter_position_counts[c][i] += 1
        ranked_word_dict = {}
        for word in word_list:
            word_ranking = 0
            for i, c in enumerate(word):
                word_ranking += letter_position_counts[c][i]
            ranked_word_dict[word] = word_ranking
            # Penalize any word with repeated letters
            if not cls.allow_duplicates and len(set(word)) < len(word):
                ranked_word_dict[word] //= 2
        return ranked_word_dict

    @classmethod
    def get_suggested_word(cls, possible_words: List[str]) -> str:
        return cls.get_suggested_word_highest(possible_words)


def get_word_list(dictionary_path, limit_to_letters=None):
    with open(dictionary_path) as f:
        if limit_to_letters:
            return [word.strip("\n").lower() for word in f.readlines() if len(word) == limit_to_letters + 1]
        else:
            return load(f)


def get_possible_words(
        word_list: List[str],
        correct_letters: List[str],
        extra_letters: Set[str],
        incorrect_letters: Set[str],
        wrong_positions: Dict[str, List[int]],
) -> List[str]:
    possible_words = []
    for word in word_list:
        extra_letters_to_check = set()
        for i, c in enumerate(word):
            if correct_letters[i]:
                if correct_letters[i] == c:
                    # Good letter, check next letter
                    continue
                else:
                    # Doesn't match known letter, go to next word
                    break
            if c in incorrect_letters:
                # Bad letter, go to next word
                break
            if c in wrong_positions and i in wrong_positions[c]:
                # Letter was already tried in this spot, go to next word
                break
            extra_letters_to_check.add(c)
        else:
            if not extra_letters.difference(extra_letters_to_check):
                possible_words.append(word)
    return possible_words


def print_words(possible_words, words_per_line=10, max_words=100):
    print("")
    print("{} possible words".format(len(possible_words)))
    if len(possible_words) < max_words:
        for i in range(int(len(possible_words) / words_per_line) + 1):
            print(", ".join(possible_words[i * words_per_line:(i + 1) * words_per_line]))


def check_status(status: str, word_input: str, wrong_positions: Dict[str, List[int]]):
    correct_letters = [""] * len(word_input)
    extra_letters = set()
    incorrect_letters = set()
    wrong_positions = deepcopy(wrong_positions)
    for i, s in enumerate(status):
        c = word_input[i]
        if s == "y":
            correct_letters[i] = c
        elif s == "n":
            if c not in wrong_positions:
                incorrect_letters.add(c)
        elif s == "m":
            extra_letters.add(c)
            wrong_positions[word_input[i]].append(i)
        else:
            return None
    return correct_letters, extra_letters, incorrect_letters, wrong_positions


def prompt_for_input(suggested_word: str, incorrect_letters: Set[str], wrong_positions: Dict[str, List[int]]):
    while True:
        print("")
        print("Suggested word: {}".format(suggested_word))
        print("")
        status = input("Result of each letter (y, n, m; blank to enter different word than suggested): ")
        word_input = suggested_word
        if status == "":
            word_input = input("What word did you try? ")
            status = input("Result of each letter (y, n, m): ")
        if len(status) != len(word_input):
            print("That result doesn't match the word given. Let's try again...")
            continue
        status_check_result = check_status(status, word_input, wrong_positions)
        if status_check_result:
            c, e, i, w = status_check_result
            incorrect_letters.update(i)
            return c, e, incorrect_letters, w


def main():
    game = "wordle"
    # game = "lewdle"
    # game = "nerdle"
    word_list = get_word_list(f"{game}_dictionary.json")
    # word_list = get_word_list("scrabble_dictionary.txt", limit_to_letters=11)
    print(len(word_list))
    correct_letters = [""] * len(word_list[0])
    incorrect_letters = set()
    extra_letters = set()
    wrong_positions = defaultdict(list)
    strategy = MostCommonPositionsStrategy
    strategy.allow_duplicates = False

    try:
        while True:
            possible_words = get_possible_words(
                word_list, correct_letters, extra_letters, incorrect_letters, wrong_positions
            )
            # if not possible_words:
            #     # Something happened that caused the list of possible words to be empty. Perhaps the user guessed
            #     # a word not in the previous list of possible words. This should be allowed, so we'll just rerun on
            #     # the whole list.
            #     print("Rerunning on list of all words")
            #     print(len(all_word_list))
            #     possible_words = get_possible_words(
            #         all_word_list, correct_letters, extra_letters, incorrect_letters, wrong_positions
            #     )
            print_words(possible_words)
            suggested_word = strategy.get_suggested_word(possible_words)
            correct_letters, extra_letters, incorrect_letters, wrong_positions = prompt_for_input(
                suggested_word, incorrect_letters, wrong_positions
            )
            if all(correct_letters):
                print("")
                print("You win!")
                return
            print(correct_letters)
            print(extra_letters)
            print(incorrect_letters)
            print(wrong_positions)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
