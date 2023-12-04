from src.utils import read_text
import re

p1_example = read_text("./src/day_04/p1_example.txt")
full_input = read_text("./src/day_04/full_input.txt")

def get_scores(input): 
    loop_results = []
    for i, element in enumerate(input):
        split_by_colon = element.split(": ")
        card_num = split_by_colon[0]
        numbers = split_by_colon[1]
        split_by_pipe = numbers.split(" | ")
        first_set = set(re.split(r"\s+", split_by_pipe[0]))
        first_set.discard("")
        second_set = set(re.split(r"\s+", split_by_pipe[1]))
        second_set.discard("")
        winning_nums = first_set.intersection(second_set)
        length_of_winning_nums = len(winning_nums)
        if length_of_winning_nums == 0:
            score = 0
        elif length_of_winning_nums == 1:
            score = 1
        elif length_of_winning_nums > 1:
            score = 2**(length_of_winning_nums-1)
        else:
            raise ValueError(f"Invalid length_of_winning_nums: {length_of_winning_nums}")
        loop_results.append(score)
    return(loop_results)

p1_example_scores = get_scores(p1_example)        
print(f"Sum of p1_example_scores: {sum(p1_example_scores)}")

p1_full_scores = get_scores(full_input)
print(f"Sum of p1 full scores: {sum(p1_full_scores)}")