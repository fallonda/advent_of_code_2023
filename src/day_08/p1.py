from src.utils import read_text
from itertools import cycle

example_1 = read_text("./src/day_08/example_1.txt")
example_2 = read_text("./src/day_08/example_2.txt")
full_input = read_text("./src/day_08/full_input.txt")

def convert_input(input):
    # Instructions
    instructions =  input[0].rstrip()
    # Convert maps
    rem_ws = input[1:]
    rem_ws = [x for x in rem_ws if x != "\n"]
    map_dict = {}
    for i in rem_ws:
        j = i.rstrip().split(" = ")
        key = j[0]
        left_map = j[1].split(", ")[0][1:]
        right_map = j[1].split(", ")[1][:3]
        map_dict[key] = (left_map, right_map)
    return(instructions, map_dict)

example_1_inst, example_1_map = convert_input(example_1)
example_2_inst, example_2_map = convert_input(example_2)
full_input_inst, full_input_map = convert_input(full_input)

def nav_map(instructions, map_dict) -> int:
    moves = 0
    pool = cycle(instructions)
    pos = "AAA"
    while pos != "ZZZ":
        # Next instruction
        next_inst = next(pool)
        if next_inst == "L":
            tuple_idx = 0
        elif next_inst == "R":
            tuple_idx = 1
        else:
            ValueError("Not L or R found in next instruction position.")
        # Make a move and update pos
        pos = map_dict[pos][tuple_idx]
        moves += 1
    return(moves)

nav_map(example_1_inst, example_1_map)
nav_map(example_2_inst, example_2_map)
nav_map(full_input_inst, full_input_map)
    