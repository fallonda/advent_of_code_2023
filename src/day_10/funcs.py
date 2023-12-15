import numpy as np

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


class Animal:
    def __init__(self, maze: np.array):
        self.maze = maze
        self.size = self.maze.shape
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
        
    def first_move(self, dir=0):
        # Update position
        first_move_index = [i for i,x in enumerate(self.get_first_allowed_moves()) if x is True][dir]
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
            # print(f"Moves: {self.moves}, Char: {self.char}, pos: {self.pos}.")
            self.subsequent_move()
        # Finish
        print(f"Back at '{self.char}'.")
        print(f"Moves taken: {self.moves}.")
        
    def correct_edges(self):
        # Remove the duplication of the start position.
        print(f"Length of edges before correction: {len(self.edges)}") 
        self.edges = self.edges[:-1] # Remove last element. 
        print(f"Length of edges after correction: {len(self.edges)}")
    
    def create_binary_maze(self):
        self.binary_maze = np.zeros(self.maze.shape)
        for i in self.edges:
            self.binary_maze[i] = 1
    
    def fill_tile_types(self):
        self.tile_type = []
        for i, edge in enumerate(self.edges):
            #print(i)
            if i == 0:
                self.tile_type.append("start")
            elif (i > 0) & (i < len(self.edges)-1):
                one = np.array(self.edges[i-1])
                two = np.array(self.edges[i])
                three = np.array(self.edges[i+1])
                down = np.array([1,0])
                up = np.array([-1,0])
                left = np.array([0,-1])
                right = np.array([0,1])
                two_minus_one = two - one
                three_minus_two = three - two
                if (one[0]==two[0]==three[0]):
                    if three[1] > one[1]:
                        self.tile_type.append("horizontal_going_right")
                    else:
                        self.tile_type.append("horizontal_going_left")
                elif (one[1]==two[1]==three[1]):
                    if three[0] > one[0]:
                        self.tile_type.append("vertical_going_down")
                    else:
                        self.tile_type.append("vertical_going_up")
                elif (np.array_equal(two_minus_one, left))&(np.array_equal(three_minus_two, down)):
                    self.tile_type.append("left_down")
                elif (np.array_equal(two_minus_one, left))&(np.array_equal(three_minus_two, up)):
                    self.tile_type.append("left_up")
                elif (np.array_equal(two_minus_one, right))&(np.array_equal(three_minus_two, down)):
                    self.tile_type.append("right_down")
                elif (np.array_equal(two_minus_one, right))&(np.array_equal(three_minus_two, up)):
                    self.tile_type.append("right_up")
                elif (np.array_equal(two_minus_one, down))&(np.array_equal(three_minus_two, left)):
                    self.tile_type.append("down_left")
                elif (np.array_equal(two_minus_one, down))&(np.array_equal(three_minus_two, right)):
                    self.tile_type.append("down_right")
                elif (np.array_equal(two_minus_one, up))&(np.array_equal(three_minus_two, left)):
                    self.tile_type.append("up_left")
                elif (np.array_equal(two_minus_one, up))&(np.array_equal(three_minus_two, right)):
                    self.tile_type.append("up_right")
                else:
                    raise ValueError(f"Unknown tile type at {edge}")
            elif i == len(self.edges)-1:
                self.tile_type.append("end")
            else:
                raise ValueError("Something wrong with indexing.")
            
    def go_one_left(self, edge:tuple) -> tuple:
        new_pos = (edge[0], edge[1]-1)
        return new_pos
    
    def go_one_right(self, edge):
        new_pos = (edge[0], edge[1]+1)
        return new_pos
    
    def go_one_up(self, edge):
        new_pos = (edge[0]-1, edge[1])
        return new_pos
    
    def go_one_down(self, edge):
        new_pos = (edge[0]+1, edge[1])
        return new_pos
    
    def no_move(self, edge):
        return edge
            
    def create_adj_dict(self):
        # Update which elements to track (on RHS) for area
        self.adj_dict = {
            "start": [self.no_move],
            "horizontal_going_left": [self.go_one_up],
            "horizontal_going_right": [self.go_one_down],
            "vertical_going_down": [self.go_one_left],
            "vertical_going_up": [self.go_one_right],
            "left_down": [self.go_one_up, self.go_one_left],
            "left_up": [self.no_move],
            "right_down": [self.no_move],
            "right_up": [self.go_one_down, self.go_one_right],
            "down_left": [self.no_move],
            "down_right": [self.go_one_left, self.go_one_down],
            "up_left": [self.go_one_up, self.go_one_right],
            "up_right": [self.no_move],
            "end": [self.no_move]
        }
    
    def fill_rhs_pos(self):
        self.rhs_pos = []
        self.create_adj_dict()
        for i, edge in enumerate(self.edges):
            funcs_to_apply = self.adj_dict[self.tile_type[i]]
            for j in funcs_to_apply:
                self.rhs_pos.append(j(edge))
                
    def take_unique_rhs(self):
        self.unique_rhs = list(set([x for x in self.rhs_pos if x not in self.edges]))
    
    def get_seeds(self):
        self.fill_tile_types()
        self.fill_rhs_pos()
        self.take_unique_rhs()
        return self.unique_rhs
    
    def run_all(self, dir=0):
        self.first_move(dir)
        self.move_until_end()
        self.correct_edges()
        self.create_binary_maze()
        self.get_seeds()