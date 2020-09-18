# Solver for a puzzle where cubes are attached at right angles to each other via a string, and the goal is to
# turn the cubes into a larger cube
# https://qph.fs.quoracdn.net/main-qimg-a66c6f46e8e4b2b4bf8736ad87feb692.webp

from copy import deepcopy

i = [3, 2, 2, 3, 2, 3, 2, 2, 3, 3, 2, 2, 2, 3, 3, 3, 3]
starting_pos = [0, 0, 0]


def build_cube(h=3, w=3, d=3):
    return [[[False for _ in range(h)] for _ in range(w)] for _ in range(d)]


def print_cube(cube):
    for layer in cube:
        for row in layer:
            print(" ".join(["O" if cell else "." for cell in row]))
        print("")


def find_next_placement(cube, pos, length):
    """

    :param cube: Current cube state
    :param pos: 3-tuple of ints representing place to start
    :param length: length of segments to check for
    :return:
    """


cube = build_cube()
print_cube(cube)

