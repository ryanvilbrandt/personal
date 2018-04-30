# class Test:
#     def our_decorator(self, func):
#         print("Doing stuff before the function")
#
#         def function_wrapper(self, x):
#             print("Before calling " + func.__name__)
#             res = func(self, x)
#             print(res)
#             print("After calling " + func.__name__)
#
#         return function_wrapper
#
#     @our_decorator
#     def succ(self, n):
#         return n + 1
# Ellipsis
# t = Test()
# t.succ(10)






def trapezoid_bullshit(func, start, end, intervals):
    delta_x = (end - start) / intervals
    total = func(start) / 2
    for i in range(1, intervals):
        # print(delta_x * i)
        total += func(start + (delta_x * i))
    total += func(end) / 2
    return total * delta_x

def line(x):
    return x**2

print(trapezoid_bullshit(line, 0, 10, 10))
