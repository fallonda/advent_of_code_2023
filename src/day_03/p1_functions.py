from src.utils import read_in_as_array
import numpy as np
import re

def find_part_numbers(array: np.array) -> list:
    """Process array to get list of part numbers and
    match details."""
    # Setup required variables.
    max_length = len(array[0])-1
    max_depth = array.shape[0]-1
    str_numbers = [str(x) for x in range(0,10)]
    numbers_or_dots = str_numbers.copy()
    numbers_or_dots.append(".")
    
    # Get number locations
    number_locations = []
    for row_num, row in enumerate(array):
        for i in re.finditer(r"[0-9]+", row):
            number_locations.append({
                "row": row_num,
                "start_pos": i.span()[0],
                "end_pos": i.span()[1]-1,
                "number": i.group()
            })
    
    # Get matches
    for i in number_locations:
    # Top general cases
        top_bottom_left_limit = max(i["start_pos"]-1, 0)
        top_bottom_right_limit = min(i["end_pos"]+1, max_length)+1
        i["left_limit"] = top_bottom_left_limit
        i["right_limit"] = top_bottom_right_limit
        # left edge cases
        if i["start_pos"] == 0:
            i["left"] = False
        else:
            # left general cases
            if array[i["row"]][i["start_pos"]-1] in numbers_or_dots:
                i["left"] = False
            else:
                i["left"] = True
        # right edge cases
        if i["end_pos"] == max_length:
            i["right"] = False
        else:
            # right general cases
            if array[i["row"]][i["end_pos"]+1] in numbers_or_dots:
                i["right"] = False
            else:
                i["right"] = True
        # Top edge cases
        if i["row"] == 0:
            i["top"] = False
        else:
            any_top_matches = []
            for j in array[i["row"]-1][top_bottom_left_limit:top_bottom_right_limit]:
                if j in numbers_or_dots:
                    any_top_matches.append(True)
                else:
                    any_top_matches.append(False)
            if all(any_top_matches):
                i["top"] = False
            else:
                i["top"] = True
        # Bottom edge cases
        if i["row"] == max_depth:
            i["bottom"] = False
        else:
            any_bottom_matches = []
            # bottom general cases
            for j in array[i["row"]+1][top_bottom_left_limit:top_bottom_right_limit]:
                if j in numbers_or_dots:
                    any_bottom_matches.append(True)
                else:
                    any_bottom_matches.append(False)
            if all(any_bottom_matches):
                i["bottom"] = False
            else:
                i["bottom"] = True
    return number_locations

def filter_to_part_numbers_and_sum(input: list) -> tuple:
    parts_list = []
    for i in input:
        if any([
            i["left"],
            i["right"],
            i["top"],
            i["bottom"]
        ]):
            parts_list.append(int(i["number"]))
    return (parts_list, sum(parts_list))

def run_all(path):
    lines_in = read_in_as_array(path)
    locations = find_part_numbers(lines_in)
    results = filter_to_part_numbers_and_sum(locations)
    return results