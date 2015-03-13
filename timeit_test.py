import timeit, random

statement1 = '''
for i in gen1(master, slave):
    pass
'''
statement2 = '''
for i in gen2(master, slave):
    pass
'''
statement3 = '''
for i in gen3(master, slave):
    pass
'''
statement4 = '''
for i in gen4(master, slave):
    pass
'''

setup = '''
import random

master = range(100)
#slave = set([9, 17, 229, 678, 1457, 3893, 8979, 103843])
slave = set([9, 17, 22, 67, 14, 38, 89, 103])

def gen1(a, b):
    #c = set(b)
    for _ in a:
        if not _ in b:
            yield _

def gen2(a, b):
    #c = set(b)
    return [_ for _ in a if not _ in b]

def gen3(a, b):
    #c = set(b)
    for i in [_ for _ in a if not _ in b]:
        yield i

def gen4(a, b):
    return_list = []
    #c = set(b)
    for _ in a:
        if not _ in b:
            return_list.append(_)
    return return_list
'''

print timeit.timeit(statement1, setup, number = 10000)
print timeit.timeit(statement2, setup, number = 10000)
print timeit.timeit(statement3, setup, number = 10000)
print timeit.timeit(statement4, setup, number = 10000)
