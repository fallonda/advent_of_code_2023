from src.utils import read_text
import numpy as np
from io import StringIO
from time import time
import os
import ray

os.environ["RAY_DEDUP_LOGS"] = "0"


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



def get_seeds_for_p2(p1_seeds: list) -> list:
    # Return list of ranges. 
    start_seeds = [x for i,x in enumerate(p1_seeds) if i%2 == 0]
    out_by = [x for i,x in enumerate(p1_seeds) if i%2 == 1]
    p2_seeds = []
    for i, seed in enumerate(start_seeds):
        p2_seeds.append(
            range(seed, seed+out_by[i])
        )
    return p2_seeds

example_seeds = get_seeds(p1_example)
p2_example_seeds = get_seeds_for_p2(example_seeds)

full_seeds = get_seeds(full_input)
p2_full_seeds = get_seeds_for_p2(full_seeds)
    
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
        if (current_num >= source_start) & (current_num < source_start+out_by):
            # print("New_num_found!")
            index_pos = new_num - source_start
            # print(f"index_pos: {index_pos}")
            new_num = dest_start + index_pos
            return new_num
        # else:
        #     print("No new num found.")
    return new_num

def map_backwards(current_num: int, list_of_arrays: list) -> int:
    for i in list_of_arrays:
        source_start, dest_start, out_by = i # Different order
        new_num = current_num # Default
        # Update it if there is a match: 
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
map_backwards(4, [np.array([1,2,3])])
map_backwards(2, [np.array([1,2,2])])

def map_seed_to_location(seed: int, mapping_dict: dict) -> int:
    current_num = seed
    for key, value in mapping_dict.items():
        #print(f"For: {key}")
        #print(f"Current_num: {current_num}")
        current_num = get_next_number(current_num, list_of_arrays = value)
        #print(f"After mapping: {current_num} \n")
    return current_num

def map_location_to_seed(location: int, mapping_dict: dict) -> int:
    # returns a location int for a given seed int. 
    current_num = location
    rev_dict = dict(reversed(list(mapping_dict.items())))
    for key, value in rev_dict.items():
        # print(f"For: {key}")
        # print(f"Current_num: {current_num}")
        current_num = map_backwards(current_num, list_of_arrays = value)
        # print(f"After mapping: {current_num} \n")
    return current_num

# test it
# map_location_to_seed(82, example_mapping_dict) # Excellent!

def check_if_seed_exists(seed: int, ranges: list) -> bool:
    for i in ranges:
        min_val = i[0]
        max_val = i[-1]
        if (seed >= min_val) & (seed < max_val):
            print(f"Seed '{seed}' found in range: {i}!!!")
            return True
        else:
            return False
        
# test it
# check_if_seed_exists(89, p2_example_seeds)

ray.init()

# Check for seed existance starting with location
@ray.remote
def search_for_seeds(loc_range, ranges, mapping_dict):
    start_time = time()
    num_length_counter = 1
    for loc in loc_range:
        if len(str(loc)) == num_length_counter:
            print(f"Counter: {loc}")
            end_time = time()
            time_taken = end_time - start_time
            print(f"Time taken: {round(time_taken/60, 2)} min.")
            num_length_counter += 1
        # print(f"mapping seed for location {loc}")
        seed = map_location_to_seed(loc, mapping_dict)
        # print(f"Checking if seed {seed} exists.")
        seed_exists = check_if_seed_exists(seed, ranges)
        if (seed_exists): # gives T/F
            print(f"Seed: {seed}, Location: {loc}")
            end_time = time()
            time_taken = end_time - start_time
            print(f"Time taken: {round(time_taken/60, 2)} min.")
            raise ValueError("Run complete:")

# test it on example
# search_for_seeds(range(80), p2_example_seeds, example_mapping_dict)

RAY_DEDUP_LOGS=0

full_search_range = range(int(1e18))
split_by = 8
split_ranges = []
for i in range(split_by):
    sub_range = full_search_range[i::split_by]
    split_ranges.append(sub_range)
    
# Run on full input using ray. 
results = [search_for_seeds.remote(i, p2_full_seeds, full_mapping_dict) for i in split_ranges]