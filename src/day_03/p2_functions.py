import numpy as np
import re
import pandas as pd

def find_gears(array: np.array) -> list:
    """Process array to get list of part numbers that are 
    beside gears."""
    # Setup required variables.
    max_length = len(array[0])-1
    max_depth = array.shape[0]-1
    
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
            if array[i["row"]][i["start_pos"]-1] == "*":
                i["left"] = True
                i["gear_pos"] = (i["row"], i["start_pos"]-1)
            else:
                i["left"] = False
        # right edge cases
        if i["end_pos"] == max_length:
            i["right"] = False
        else:
            # right general cases
            if array[i["row"]][i["end_pos"]+1] == "*":
                i["right"] = True
                i["gear_pos"] = (i["row"], i["end_pos"]+1)
            else:
                i["right"] = False
        # Top edge cases
        if i["row"] == 0:
            i["top"] = False
        else:
            any_top_matches = []
            for j in range(top_bottom_left_limit, top_bottom_right_limit):
                if array[i["row"]-1][j] == "*":
                    any_top_matches.append(True)
                    i["gear_pos"] = (i["row"]-1, j)
                else:
                    any_top_matches.append(False)
            if any(any_top_matches):
                i["top"] = True
            else:
                i["top"] = False
        # Bottom edge cases
        if i["row"] == max_depth:
            i["bottom"] = False
        else:
            any_bottom_matches = []
            # bottom general cases
            for j in range(top_bottom_left_limit, top_bottom_right_limit):
                if array[i["row"]+1][j] == "*":
                    any_bottom_matches.append(True)
                    i["gear_pos"] = (i["row"]+1, j)
                else:
                    any_bottom_matches.append(False)
            if any(any_bottom_matches):
                i["bottom"] = True
            else:
                i["bottom"] = False
    return number_locations


def filter_to_gears_only(input: list) -> tuple:
    parts_list = []
    for i in input:
        if any([
            i["left"],
            i["right"],
            i["top"],
            i["bottom"]
        ]):
            parts_list.append(i)
    return (parts_list)



