from day_03.p1_functions import (
    run_all,
    find_part_numbers,
    filter_to_part_numbers_and_sum
)
from src.utils import read_in_as_array

p1_example_results = run_all("./src/day_03/part_1_example.txt")
print(p1_example_results)


p1_in = read_in_as_array("./src/day_03/full_input.txt")
p1_locations = find_part_numbers(p1_in)
p1_full = filter_to_part_numbers_and_sum(p1_locations)
print(p1_full)