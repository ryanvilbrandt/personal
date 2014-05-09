import time

d = {}
BLANK_SYMBOL = "0"
d['0'] = {'A': ('1','R','B'), 'B': ('1','L','A'), 'C': ('1','L','B')}
d['1'] = {'A': ('1','L','C'), 'B': ('1','R','B'), 'C': ('1','R','H')}
TAPE_SIZE = 16
tape = [BLANK_SYMBOL]*TAPE_SIZE
START_INDEX = TAPE_SIZE/2
START_STATE = "A"
END_STATE = "H"
DELAY = 1

def PrintTape(tape, index):
    print " ".join(tape)
    print index*"  "+"^"

state = START_STATE
index = START_INDEX
while not state == END_STATE:
    PrintTape(tape, index)
    time.sleep(DELAY)
    read_symbol = tape[index]
    current_instructions = d[read_symbol][state]
    print "{0}{1}: {2}".format(state, read_symbol, current_instructions)
    tape[index] = current_instructions[0]
    if current_instructions[1] == "R":
        index += 1
        index = index % TAPE_SIZE
    elif current_instructions[1] == "L":
        index -= 1
        index = index % TAPE_SIZE
    state = current_instructions[2]    
    
PrintTape(tape, index)
