# http://spikedmath.com/574.html
# Step 1: Take any four digit number that is not 1111, 2222, 3333 ...
# Step 2: Organize the digits so that they're organized in ascending order, and then descending order
# Step 3: Subtract the smaller number from the larger number
# Step 4: Repeat until the number stops changing

import random

def step2and3(num):
    '''@param int num'''
    num_list = map(str, sorted(map(int, list("{:>04}".format(num)))))
    small_num = int("".join(num_list))
    num_list.reverse()
    large_num = int("".join(num_list))
    return large_num - small_num

def stepCycle(num):
    iter = 0
    old_num = 0
    while True:
        iter += 1
        num = step2and3(num)
        if num == old_num:
            return num, iter
        old_num = num


print stepCycle(random.randint(1, 10000))
