from src.utils import read_text
import numpy as np
from io import StringIO
import pandas as pd

p1_example = read_text("./src/day_05/p1_example.txt")
p1_example.extend("\n")

full_input = read_text("./src/day_05/full_input.txt")
full_input.extend("\n")

def get_seeds(input: list) -> list:
    seeds = np.loadtxt(
        fname = StringIO(input[0].split(": ")[1]),
        dtype = int
    )
    return seeds

example_seeds = get_seeds(p1_example)
full_seeds = get_seeds(full_input)
    
def get_ranges(input: list) -> dict:
    maps = {}
    for i, line in enumerate(input):
        if "map:" in line:
            title = line.split(" ")[0]
            mapping_list = []
            j = 1
            while input[i+j][0] != "\n":
                mapping_list.append(
                    np.loadtxt(
                        fname = StringIO(input[i+j]),
                        dtype = int
                    )
                )
                j += 1
            maps[title] = mapping_list
    return maps

example_mapping_dict = get_ranges(p1_example)
full_mapping_dict = get_ranges(full_input)

def get_next_number(current_num: int, list_of_arrays: list) -> int:
    for i in list_of_arrays:
        dest_start, source_start, out_by = i
        new_num = current_num # Default
        # Update it if there is a match: 
        range_to_check = range(source_start, source_start+out_by)
        # print(f"range_to_check: {range_to_check}")
        if (current_num >= source_start) & (current_num < source_start+out_by):
            # print("New_num_found!")
            index_pos = new_num - source_start
            # print(f"index_pos: {index_pos}")
            new_num = dest_start + index_pos
            return new_num
        # else:
        #     print("No new num found.")
    return new_num

# test it
get_next_number(4, [np.array([1,2,3])])
get_next_number(4, [np.array([1,2,2])])

def map_seed_to_location(seed: int, mapping_dict: dict) -> int:
    current_num = seed
    for key, value in mapping_dict.items():
        print(f"For: {key}")
        print(f"Current_num: {current_num}")
        current_num = get_next_number(current_num, list_of_arrays = value)
        print(f"After mapping: {current_num} \n")
    return current_num

# test it
def get_all_locations(seeds, mapping_dict):
    locations = []
    for seed in seeds:
        # print(seed)
        loc = map_seed_to_location(seed, mapping_dict)
        locations.append(loc)
    min_loc = min(locations)
    return locations, min_loc

example_locations = get_all_locations(example_seeds, example_mapping_dict)
print(example_locations)
full_locations = get_all_locations(full_seeds, full_mapping_dict)
print(full_locations)
