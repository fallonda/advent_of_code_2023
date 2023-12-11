from src.utils import read_in_as_array
from math import prod

example_in = read_in_as_array("./src/day_06/example.txt")

def get_time_and_dist(array) -> list:
    # Return list of tuples: [(time, dist)...]
    time = int("".join(array[0][1:]))
    dist = int("".join(array[1][1:]))
    return (time, dist)
    
example_time_and_dist = get_time_and_dist(example_in)
example_time_and_dist

def count_wins(time: int, dist: int) -> int:
    wins = 0
    for i in range(time+1):
        time_remaining = time - i
        distance_travelled = time_remaining * i
        if distance_travelled > dist:
            wins += 1
    return wins

def get_all_wins(time_and_dist: list) -> list:
    list_wins = []
    for time, dist in [time_and_dist]:
        list_wins.append(count_wins(time, dist))
    return(list_wins)

# Example result:
prod(get_all_wins(example_time_and_dist))

# Part 1:
full_input = read_in_as_array("./src/day_06/full_input.txt")
full_time_and_dist = get_time_and_dist(full_input)
prod(get_all_wins(full_time_and_dist))