from src.utils import read_in_as_array
import numpy as np
from math import ceil

example = read_in_as_array("./src/day_10/example.txt")
example = np.array([[y for y in x] for x in example])
print(example)

def pad_array(input):
    # Sides first
    height = input.shape[0]
    sides = np.zeros((height, 1), dtype = int)
    sides_added = np.hstack([sides, input, sides])
    # Top and bottom
    new_width = sides_added.shape[1]
    tb = np.zeros((1, new_width), dtype = int)
    tb_added = np.vstack([tb, sides_added, tb])
    return tb_added

padded_eg = pad_array(example)

class Animal:
    def __init__(self, maze: np.array):
        self.maze = maze
        self.start_pos = tuple(
            [x[0] for x in np.where(self.maze == "S")]
        )
        self.pos = self.start_pos
        self.char = "S"
        self.moves = -1
        self.edges = []
        # Update surroundings
        self.update_all()
        
        
    def new_positions(self):
        self.one_up = (self.pos[0]-1, self.pos[1])
        self.one_left = (self.pos[0], self.pos[1]-1)
        self.one_right = (self.pos[0], self.pos[1]+1)
        self.one_down = (self.pos[0]+1, self.pos[1])
        
    def new_chars(self):
        self.top_char = self.maze[self.one_up]
        self.left_char = self.maze[self.one_left]
        self.right_char = self.maze[self.one_right]
        self.bottom_char = self.maze[self.one_down]
    
    def update_movement_dict(self):
        self.movement_dict = {
            "J": [self.one_left, self.one_up],
            "|": [self.one_up, self.one_down],
            "-": [self.one_left, self.one_right],
            "7": [self.one_left, self.one_down],
            "F": [self.one_right, self.one_down],
            "L": [self.one_up, self.one_right]
        }
    
    def update_all(self):
        self.moves += 1
        self.char = self.maze[self.pos]
        self.new_positions()
        self.new_chars()
        self.update_movement_dict()
        self.edges.append(self.pos)
            
    def get_first_allowed_moves(self):
        self.top_allowed = self.top_char in ["|", "7", "F"]
        self.left_allowed = self.left_char in ["L", "-", "F"]
        self.right_allowed = self.right_char in ["J", "-", "7"]
        self.bottom_allowed = self.bottom_char in ["|", "L", "J"]
        return (
            self.top_allowed,
            self.left_allowed,
            self.right_allowed,
            self.bottom_allowed
        )
        
    def first_move(self):
        # Update position
        first_move_index = self.get_first_allowed_moves().index(True)
        first_moves = [
            self.one_up,
            self.one_left,
            self.one_right,
            self.one_down
        ]
        self.last_pos = self.pos
        self.pos = first_moves[first_move_index]
        # Update new surroundings
        self.update_all()
        
    def subsequent_move(self):
        char_moves = self.movement_dict[self.char]
        new_pos = [x for x in char_moves if x != self.last_pos][0]
        self.last_pos = self.pos
        self.pos = new_pos
        self.update_all()
        
    def move_until_end(self):
        while self.char != "S":
            print(f"Moves: {self.moves}, Char: {self.char}, pos: {self.pos}.")
            self.subsequent_move()
        # Finish
        print(f"Back at '{self.char}'.")
        print(f"Moves taken: {self.moves}.")
        
    def correct_edges(self):
        # Remove the duplication of the start position.
        print(f"Length of edges before correction: {len(self.edges)}") 
        self.edges = list(set(self.edges))
        print(f"Length of edges after correction: {len(self.edges)}")
    
    def create_binary_maze(self):
        print(self.maze.shape)
        
        
example_animal = Animal(padded_eg)
        
# First move
example_animal.first_move()
print(example_animal.start_pos)
print(example_animal.pos)
print(example_animal.last_pos)
# Finish remaining moves. 
example_animal.move_until_end()

half_way = ceil(example_animal.moves / 2)
print(f"Furthest point away for example: {half_way}.")

# Full input:
full_input = read_in_as_array("./src/day_10/full_input.txt")
full_input = np.array([[y for y in x] for x in full_input])

padded_full_input = pad_array(full_input)
print(padded_full_input.shape)

full_animal = Animal(padded_full_input)

# Full run
full_animal.first_move()
print(full_animal.start_pos)
print(full_animal.pos)
print(full_animal.last_pos)
full_animal.move_until_end()
full_half_way = ceil(full_animal.moves / 2)
print(f"Furthest point away for full: {full_half_way}.")

full_animal.moves
full_animal.correct_edges()

full_animal.edges
