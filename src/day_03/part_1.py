
from src.day_03.functions import read_in_as_array
import re

p1_example = read_in_as_array("./src/day_03/part_1_example.txt")

p1_example_reshaped = p1_example.reshape(-1,1)

print(p1_example)
print(p1_example_reshaped)

max_length = len(p1_example[0])-1
max_depth = p1_example.shape[0]-1

str_numbers = [str(x) for x in range(0,10)]

numbers_or_dots = str_numbers.copy()
numbers_or_dots.append(".")


number_locations = []
for row_num, row in enumerate(p1_example):
    for i in re.finditer(r"[0-9]+", row):
        number_locations.append({
            "row": row_num,
            "start_pos": i.span()[0],
            "end_pos": i.span()[1]-1,
            "number": i.group()
        })
        
print(number_locations)

    

# Check left
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
        if p1_example[i["row"]][i["start_pos"]-1] in numbers_or_dots:
            i["left"] = False
        else:
            i["left"] = True
    # right edge cases
    if i["end_pos"] == max_length:
        i["right"] == False
    else:
        # right general cases
        if p1_example[i["row"]][i["end_pos"]+1] in numbers_or_dots:
            i["right"] = False
        else:
            i["right"] = True
    # Top edge cases
    if i["row"] == 0:
        i["top"] = False
    else:
        any_top_matches = []
        for j in p1_example[i["row"]-1][top_bottom_left_limit:top_bottom_right_limit]:
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
        for j in p1_example[i["row"]+1][top_bottom_left_limit:top_bottom_right_limit]:
            if j in numbers_or_dots:
                any_bottom_matches.append(True)
            else:
                any_bottom_matches.append(False)
        if all(any_bottom_matches):
            i["bottom"] = False
        else:
            i["bottom"] = True
            
print(p1_example_reshaped)
[print(x) for x in number_locations]

parts_list = []
for i in number_locations:
    if any([
        i["left"],
        i["right"],
        i["top"],
        i["bottom"]
    ]):
        parts_list.append(int(i["number"]))
        
print(parts_list)

print(sum(parts_list))
