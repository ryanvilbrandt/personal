FLOORS = 100

def binary_death_floor(death_floor, curr_floor=-1, min_floor=0, max_floor=FLOORS + 1, count=0):
    '''
    :param death_floor: The lowest floor on which the lightbulb will break
    :param curr_floor: Current floor we're testing on
    :param min_floor: The highest floor we've currently found where the lightbulb does NOT break
    :param max_floor: The lowest floor we've currently found where the lightbulb breaks
    :param count: Number of drops attempted so far

    Binary search for the lightbulb drop problem

    :return: 2-tuple, int: The death floor as found by the algorithm, and the number of drops made
    '''
    # Have we found the final floor?
    if max_floor - min_floor == 1:
        return max_floor, count
    # Skip checking on first test
    if curr_floor > -1:
        print curr_floor,
        # Drop a lightbulb. Does it break?
        if curr_floor >= death_floor:
            print "Broke!"
            max_floor = curr_floor
        else:
            print "Safe!"
            min_floor = curr_floor
    # Next floor is the average of the min and max floors
    next_floor = (min_floor + max_floor) / 2
    # Increment count by 1
    return binary_death_floor(death_floor, next_floor, min_floor, max_floor, count + 1)

def step_death_floor(death_floor):
    # Which floors are my "milestones" as I go up?
    # I start at 14, then increment by 13, then 12, then 11...
    # Because 1 + 2 + 3 ... + 13 + 14 = 105
    floor_steps = [14, 27, 39, 50, 60, 69, 77, 84, 90, 95, 99]
    last_floor = 0
    count = 0
    for floor_1 in floor_steps:
        count += 1
        if floor_1 >= death_floor:
            break
        last_floor = floor_1
    else:
        # The lightbulb didn't drop on any of the floors.
        # Test once more on the 100th floor and report results
        count += 1
        if 100 == death_floor:
            # It broke!
            return 100, count
        else:
            # It didn't break
            return 101, count
    # The lightbulb broke! Go to the last floor it didn't break, and increment by one until it does
    # Don't retest the last floor where it broke.
    for floor_2 in xrange(last_floor + 1, floor_1):
        count += 1
        if floor_2 >= death_floor:
            # The lightbulb broke! Return the current floor
            return floor_2, count
    else:
        # The lightbulb didn't break! That means that the next floor we would test
        # is the death floor. Return that.
        return floor_2 + 1, count

with open('step_bulbs.csv', 'w') as f:
    # Testing up to 101, because it's possible the lightbulb will not break on the 100th
    for i in xrange(1, FLOORS+2):
        results = step_death_floor(i)
        f.write("{},{}\n".format(*results))
        print results

