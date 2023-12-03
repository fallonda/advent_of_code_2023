from src.utils import (
    read_in_as_array
)
from src.day_03.p2_functions import (
    find_gears,
    filter_to_gears_only,
    get_product_and_sum
)

example = read_in_as_array("./src/day_03/part_1_example.txt")
example_reshaped = example.reshape(-1,1)

example_locations = find_gears(example)
example_gears_only = filter_to_gears_only(example_locations)

example_result = get_product_and_sum(example_gears_only)
print(example_result)

# Part 2 on full input
full_input = read_in_as_array("./src/day_03/full_input.txt")
full_locations = find_gears(full_input)
full_gears_only = filter_to_gears_only(full_locations)
full_result = get_product_and_sum(full_gears_only)
print(full_result)