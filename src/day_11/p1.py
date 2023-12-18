from src.utils import read_in_as_array
import numpy as np

def read_in_and_split(path: str) -> np.array:
    # Read in the file and split into array of 
    # individual characters. 
    file_in = read_in_as_array(path).reshape(-1,1)
    split_list = []
    for i in file_in:
        split_list.extend([[y for y in x] for x in i])
    return np.array(split_list)

ex = read_in_and_split("./src/day_11/example.txt")

def insert_space(array: np.array) -> np.array:
    internal_array = array.copy()
    rows = [i for i, x in enumerate(array) if all(x == ".")]
    print(f"Shape of input: {array.shape}")
    inserted_rows = np.insert(array, rows, "o", axis = 0)
    print(f"Shape after inserting rows: {inserted_rows.shape}")
    columns = [i for i, x in enumerate(array.T) if all(x == ".")]
    inserted_columns = np.insert(inserted_rows, columns, "o", axis=1)
    print(f"Shape after inserting columns: {inserted_columns.shape}")
    return inserted_columns

ex_space = insert_space(ex)

def get_galaxy_positions(array: np.array) -> list:
    # Return list of tuples containing galaxy positions
    # [(row, col), ...]
    list_pos = []
    for i, row in enumerate(array):
        for j, col in enumerate(row):
            if col == "#":
                list_pos.append(
                    (i, j)
                )
    return list_pos

ex_pos = get_galaxy_positions(ex_space)

def get_shortest_paths(list_pos: list, array:np.array, expansion_factor:int = 1) -> list:
    shortest_paths = []
    func_list = list_pos.copy()
    while len(func_list) > 0:
        pos = func_list.pop(0)
        dists = []
        for other_pos in func_list:
            lower_row = min([pos[0], other_pos[0]])
            higher_row = max([pos[0], other_pos[0]])
            lower_col = min([pos[1], other_pos[1]])
            higher_col = max([pos[1], other_pos[1]])
            row_to_check = array[pos[0]][lower_col:higher_col]
            num_in_row = len([x for x in row_to_check if x == "o"])
            print(num_in_row)
            col_to_check = array.T[pos[1]][lower_row:higher_row]
            num_in_col = len([x for x in col_to_check if x == "o"])
            if expansion_factor > 1:
                row_diff = abs(pos[0] - other_pos[0]) + (num_in_row * (expansion_factor-1)) - num_in_row
                col_diff = abs(pos[1] - other_pos[1]) + (num_in_col * (expansion_factor-1)) - num_in_col
            else:
                row_diff = abs(pos[0] - other_pos[0])
                col_diff = abs(pos[1] - other_pos[1])
            combined_dist = sum([row_diff, col_diff])
            dists.append(combined_dist)
        shortest_paths.extend(dists)
    return shortest_paths

sum(get_shortest_paths(ex_pos, ex_space))

# Full input
full_input = read_in_and_split("./src/day_11/full_input.txt")
full_input = insert_space(full_input)
full_input = get_galaxy_positions(full_input)

sum(get_shortest_paths(full_input))