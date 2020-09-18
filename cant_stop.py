def get_column_value(n):
    return abs(n - 7) + 1


def get_modifier(columns):
    if len(columns) > 3:
        raise ValueError(columns)
    modifier = 0
    if len(columns) == 3:
        if all([c % 2 == 1 for c in columns]):
            modifier += 2
        elif all([c % 2 == 0 for c in columns]):
            modifier -= 2
        if all([c > 8 for c in columns]) or all([c < 6 for c in columns]):
            modifier += 4
    return modifier


print("Welcome to the Can't Stop helper! To use this, type the number of the column (2-12) and hit enter to indicate "
      "placing a token or advancing it. A plain Enter indicates you've stopped.\n")

columns_this_turn = set()
total = 0
while True:
    score = total + get_modifier(columns_this_turn)
    i = input("Current total {}, {} ".format(score, "keep going..." if score < 28 else "STOP!"))
    if i == "":
        print("Stopped at {} points!\n".format(score))
        columns_this_turn = set()
        total = 0
        continue
    print(i)
    num = int(i)
    multiplier = 1 if num in columns_this_turn else 2
    columns_this_turn.add(num)
    total += get_column_value(num) * multiplier
