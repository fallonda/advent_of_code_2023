from src.utils import read_text
from itertools import cycle
from math import lcm

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

full_input_inst, full_input_map = convert_input(full_input)

class Ghost:
    def __init__(self, start_pos):
        self.start_pos = start_pos
        self.pos = start_pos
        self.moves = 0
    
    def single_move(self, single_inst, map):
        if single_inst == "L":
            tuple_idx = 0
        elif single_inst == "R":
            tuple_idx = 1
        else:
            ValueError("Not L or R found in next instruction position.")
        self.pos = map[self.pos][tuple_idx]
        self.moves += 1
    
    def check_z(self):
        if self.pos[-1] == "Z":
            self.on_z = True
        else:
            self.on_z = False
        return self.on_z
    
    def go_until_z(self, inst, map):
        pool = cycle(inst)
        while not self.check_z():
            single_inst = next(pool)
            self.single_move(single_inst, map)
        print(f"Finished after {self.moves} moves.")
        return self.moves
    
# Get a starting positions and create ghosts.
a_pos = []
for key, value in full_input_map.items():
    if key[-1] == "A":
        a_pos.append(key)
ghosts = [Ghost(a) for a in a_pos]
        
ghost_moves = [a.go_until_z(full_input_inst, full_input_map) for a in ghosts]

lcm(*ghost_moves)

# # Game loop
# def nav_map(ghosts, instructions, map_dict) -> int:
#     start_time = time()
#     moves = 0
#     pool = cycle(instructions)
#     while not all([a.check_z() for a in ghosts]):
#         # Print updates
#         if moves % int(1e7) == 0:
#             print(f"Moves: {moves}")
#             end_time = time()
#             time_taken = end_time - start_time
#             print(f"Time taken: {round(time_taken/60, 2)} min.")
#         # Move the ghosts
#         next_inst = next(pool)
#         [a.single_move(next_inst, map_dict) for a in ghosts]
#         moves += 1
#     print(f"\nComplete!\n")
#     end_time = time()
#     time_taken = end_time - start_time
#     print(f"Time taken: {round(time_taken/60, 2)} min.")
#     return(moves)

# nav_map(ghosts, full_input_inst, full_input_map)