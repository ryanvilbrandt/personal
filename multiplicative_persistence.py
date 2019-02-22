starting_digit = 9223372036854775807
lower_threshold = 2222222222222222222

numbers_to_check = set()

a = [9] * 19

while a[0] > 0:
    numbers_to_check.add(tuple(a))
    print(numbers_to_check)

    if a[-1]