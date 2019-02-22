import random

def guess(x):
    out = []
    while x > 0:
        out.append(x % 34)
        x = x // 34
    print(out)

def rand_low_weight(m, n):
    """
    Picks a random number from a half-triangular distribution from m to n, inclusive,
    with the weight towards the low end.
    :param m:
    :param n:
    :return:
    """
    # Pick from random.triangular, a full triangular distribution
    temp = int(random.triangular(m,n*2-m))
    # "Fold" the full triangle in half, so the probability
    # distribution goes from low-chance at m and stops at
    # high chance at n
    if temp > n:
        temp = n*2-temp+1
    # Flip the triangle so that the high chance is near m
    # and the low chance is near n
    return n-temp+m

def main():
    n = rand_low_weight(3,7)
    p = [rand_low_weight(1,20) for _ in range(n)]

    print("I am thinking of a polynomial in x with nonnegative integer coefficients.")
    print("You can ask me the value of the polynomial at any integer value of x,")
    print("and I will tell you. Then you can do this again, as many times as you like.")
    print("When you are ready to guess my polynomial, type 'solve'. To quit, type 'quit'.")

    while True:
        r = input("\nWhat's your guess? ").lower()
        if r == "solve":
            print("\nType out your guess of the coefficients, separating each with a space.")
            print("For example, 3x^3 + x^2 + 2x + 3 would be 3 1 2 3")
    ##        print repr(r.split(' '))
    ##        print repr(p)
            while True:
                r = input()
                try:
                    last_guess = [int(x) for x in r.split(' ')]
                except ValueError as e:
                    print("That's not a valid guess. Please try again.")
                else:
                    if last_guess == p:
                        print("Correct! You win!")
                    else:
                        print("Sorry, that's wrong. My polynomial was {0}".format(p))
                    break
            break
        elif r == "quit":
            break
        else:
            try:
                guess = int(r)
            except ValueError as e:
                print("Sorry, that's not a valid guess")
            else:
                total = 0
                order = 0
                for x in p[::-1]:
                    total += x*(guess**order)
                    order += 1
                print("f({0}) = {1}".format(guess, total))

if __name__ == "__main__":
    main()
