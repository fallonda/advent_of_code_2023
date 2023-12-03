from src.utils import (
    read_in_as_array
)
from src.day_03.p2_functions import (
    find_gears,
    filter_to_gears_only
)

example = read_in_as_array("./src/day_03/part_1_example.txt")
example_reshaped = example.reshape(-1,1)

example_gears = find_gears(example)
gears_only = filter_to_gears_only(example_gears)

[{i: x[i] for i in ["gear_pos", "number"]} for x in gears_only]



print(example_reshaped)
[print(x) for x in gears_only]

