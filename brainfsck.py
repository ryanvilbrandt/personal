import sys, time

MEM_ARRAY_SIZE = 128
MEM_BITS = 64
VERBOSE = False
PRINT_CHAR = True


def print_code(in_str, codeptr, dataptr, mem, iters):
    print(in_str)
    print(" " * codeptr + "^")
    print("{} {}: {} ({} iters)".format(codeptr, dataptr, mem, iters))


def main(in_str):
    mem = [0] * MEM_ARRAY_SIZE
    codeptr = 0
    dataptr = 0
    levelarray = []
    iters = 0
    bits_mod = 1 << MEM_BITS
    while codeptr < len(in_str):
        iters += 1
        if in_str[codeptr] == ">":
            # Mod allows for circular memory buffer
            dataptr = (dataptr + 1) % MEM_ARRAY_SIZE
        elif in_str[codeptr] == "<":
            dataptr = (dataptr - 1) % MEM_ARRAY_SIZE
        elif in_str[codeptr] == "+":
            mem[dataptr] = (mem[dataptr] + 1) % bits_mod
        elif in_str[codeptr] == "-":
            mem[dataptr] = (mem[dataptr] - 1) % bits_mod
        elif in_str[codeptr] == ".":
            if PRINT_CHAR:
                sys.stdout.write(chr(mem[dataptr]))
            else:
                sys.stdout.write(str(mem[dataptr]))
        elif in_str[codeptr] == ",":
            req = None
            print("\nGive me one byte of input, use quotes for a char: ")
            while (req == None):
                req = input()
                try:
                    req = int(req) & 0xFF
                except ValueError:
                    try:
                        if req[0] == '"' or "'":
                            req = ord(req[1])
                        else:
                            print("Invalid input")
                            req = None
                    except IndexError:
                        print("Invalid input")
                        req = None
            mem[dataptr] = req
        elif in_str[codeptr] == "[":
            # If data at pointer is 0, jump to matching ]
            if mem[dataptr] == 0:
                err_ptr = codeptr
                i = 0
                # Use -1 because of oddness in code
                while i > -1:
                    codeptr += 1
                    # If the open bracket doesn't have a matching ending bracket, error out
                    if codeptr >= len(in_str):
                        print("\nEOL reached when scanning for ending bracket; unmatched [ at {}".format(err_ptr))
                        codeptr = err_ptr
                        print_code(in_str, codeptr, dataptr, mem, iters)
                        return
                    if in_str[codeptr] == "[":
                        # Keep track of "level" you're on, to make sure that ] is the proper matching bracket
                        i += 1
                    elif in_str[codeptr] == "]":
                        i -= 1
            # Else, move to next command. Save location of this [
            else:
                levelarray.append(codeptr)
        elif in_str[codeptr] == "]":
            # If data at pointer is 0, move to next command
            if mem[dataptr] == 0:
                # Remove the pointer position of the matching [
                levelarray.pop()
            # Else, jump back to matching [
            else:
                if len(levelarray) == 0:
                    print("\nFound a ] without a matching [ at {0}".format(codeptr))
                    print_code(in_str, codeptr, dataptr, mem, iters)
                    return
                codeptr = levelarray[-1]
        if VERBOSE:
            # print("")
            print_code(in_str, codeptr, dataptr, mem, iters)
            time.sleep(0.01)
        codeptr += 1

    # print("\n\n{}: {} ({} iters)".format(dataptr, mem, iters))


if __name__ == "__main__":
    # in_str = "Addition ,>,[-<+>]<."
    # in_str = "Multiplication ,>,<[>[>+>+<<-]>[<+>-]<<-]>>>."
    # in_str = "Factorial ,[->+>+<<]>>->>+<<<[>[<[->[-<<+>>>+<]>[-<+>]<<]<[->+<]>>-]<.>>>-]>>>[.-]"
    # in_str = "++++[.-]"
    in_str = open('99_bottles_of_beer.brainfuck').read()


    ##in_str = ""
    ##i = raw_input("Input brainfsck code now, type 'run' to end: ")
    ##while(i != "run"):
    ##    in_str += i
    ##    i = raw_input()
    ##in_str = in_str.replace('\n','')

    main(in_str)
