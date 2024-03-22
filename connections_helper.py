from itertools import permutations
from typing import Set, Tuple

words = ["mood", "volleyball", "hockey", "table", "breaking", "trampoline", "skeleton", "record"]

# Past guesses, and if they resulted in a "One away" message or not
hints = {
    ("mood", "breaking", "skeleton", "record"): False,
    ("mood", "volleyball", "trampoline", "skeleton"): False,
    ('hockey', 'mood', 'record', 'table'): True,
}

Groups = Tuple[Tuple[str, str, str, str]]
Groupings = Set[Groups]


def make_possible_groupings() -> Groupings:
    possible_groupings = set()
    for p in permutations(words):
        groups = []
        # Break permutation up into groups of 4. Sort and add to set to remove duplicates.
        # Example: [(a, b, c, d), (e, f, g, h)] is a duplicate of [(e, f, g, h), (a, b, c, d)]
        for i in range(0, len(p), 4):
            groups.append(tuple(sorted(p[i:i+4])))
        possible_groupings.add(tuple(sorted(groups)))
    print(len(possible_groupings))
    return possible_groupings


def apply_hints(possible_groupings: Groupings) -> Groupings:
    filtered_groupings = possible_groupings
    for guess, clue in hints.items():
        new_set = set()
        print(guess, clue)
        for grouping in filtered_groupings:
            num_groupings = len(grouping)
            counts = [0] * num_groupings
            for word in guess:
                # Check which grouping the word is in and increment that count
                for i in range(num_groupings):
                    if word in grouping[i]:
                        counts[i] += 1
                        break
            if clue and 3 in counts:
                # The clue was "One away" and one of the groups had 3 of the guessed words. Good guess.
                 new_set.add(grouping)
            elif not clue and 3 not in counts:
                # The clue was not "One away" and none of the groups had 3 of the guessed words. Good guess.
                new_set.add(grouping)
        filtered_groupings = new_set
    print(len(filtered_groupings))
    return filtered_groupings


def main():
    possible_groupings = make_possible_groupings()
    groups = apply_hints(possible_groupings)
    for group in groups:
        print(group)


if __name__ == '__main__':
    main()