from json import dump
from typing import List

VALID_PATTERNS = ['##+#+#', '#+##+#', '#+#+##']
CHARACTER_DICT = {
    "#": "1234567890",
    "N": "123456789",
    "+": "+-*/"
}


def get_all_patterns(length: int) -> List[str]:
    """
    Generates an exhaustive list of patterns that look like the left side of an arithmetic equation
    e.g. ##+#+# which could represent an equation like 12*3-4
    # = any digit, N = any digit except 0, + = any operator (+-*/)
    Guarantees each pattern begins and ends with # and no two + are right next to each other
    :param length:
    :return:
    """
    return pattern_generator("", length)


def pattern_generator(pattern_so_far: str, max_length: int) -> List[str]:
    if len(pattern_so_far) == max_length:
        # Only allow patterns that end with #
        if not pattern_so_far.endswith("#"):
            return []
        # No triple-digit or greater numbers allowed
        if "N###" in pattern_so_far:
            return []
        return [pattern_so_far]
    if pattern_so_far == "":
        c_list = ["#", "N"]
    elif pattern_so_far == "#" or pattern_so_far.endswith("+#"):
        # Zeroes are only allowed as single digit numbers
        c_list = ["+"]
    elif pattern_so_far.endswith("+"):
        c_list = ["#", "N"]
    elif pattern_so_far.endswith("N"):
        # N is only allowed at the beginning of a multi-digit number
        c_list = ["#"]
    elif pattern_so_far.endswith("#"):
        c_list = ["#", "+"]
    else:
        c_list = []
    new_list = []
    for c in c_list:
        new_list += pattern_generator(pattern_so_far + c, max_length)
    return new_list


def generate_valid_equations(length: int) -> List[str]:
    equations = []
    for solution_length in [1, 2, 3]:
        patterns = get_all_patterns(length - solution_length - 1)
        print(patterns)
        for pattern in patterns:
            print(f"Generating for pattern {pattern}")
            equations += generate_valid_equation(pattern, "", solution_length)
    return equations


def generate_valid_equation(pattern: str, equation_so_far: str, solution_length: int) -> List[str]:
    if len(equation_so_far) == len(pattern):
        solution = check_equation(equation_so_far, solution_length)
        if solution is None:
            return []
        return ["{}={}".format(equation_so_far, solution)]
    index = len(equation_so_far)
    c_type = pattern[index]
    new_list = []
    for c in CHARACTER_DICT[c_type]:
        new_list += generate_valid_equation(pattern, equation_so_far + c, solution_length)
    return new_list


def check_equation(equation: str, solution_length: int):
    try:
        solution = str(eval(equation))
    except ZeroDivisionError:
        return None
    if len(solution) == solution_length:
        return solution
    return None


equations = generate_valid_equations(8)

with open("nerdle_words.json", "w") as f:
    dump(equations, f)
