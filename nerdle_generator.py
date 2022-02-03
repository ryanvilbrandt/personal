from json import dump
from typing import List

VALID_PATTERNS = ['##+#+#', '#+##+#', '#+#+##']
CHARACTER_DICT = {
    "#": "0123456789",
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
        # Don't allow patterns that end with +
        if pattern_so_far.endswith("+"):
            return []
        # Don't allow patterns that are only digits
        if "+" not in pattern_so_far:
            return []
        # No triple-digit or greater numbers allowed
        # if "N###" in pattern_so_far:
        #     return []
        return [pattern_so_far]
    # Every number must start with a non-zero digit
    if pattern_so_far == "" or pattern_so_far.endswith("+"):
        c_list = ["N"]
    else:
        c_list = ["+", "#"]
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
        solution = eval(equation)
    except ZeroDivisionError:
        return None
    # No negative solutions allowed
    if solution < 0:
        return None
    # No solutions with fractional parts allowed
    if solution % 1 != 0:
        return None
    solution = str(int(solution))
    # Solution must fit in the remaining space
    if len(solution) != solution_length:
        return None
    return solution


equations = generate_valid_equations(8)
print(len(equations))

with open("nerdle_dictionary.json", "w") as f:
    dump(equations, f)
