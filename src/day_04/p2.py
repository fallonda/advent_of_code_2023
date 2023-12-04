from src.utils import read_text
import re
from time import sleep

p1_example = read_text("./src/day_04/p1_example.txt")
full_input = read_text("./src/day_04/full_input.txt")

def get_count_and_next_wins(input): 
    card_count = []
    wins_next = []
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
        wins_next.append(length_of_winning_nums)
        card_count.append(1)
    return(card_count, wins_next)

example_card_count, example_wins_next = get_count_and_next_wins(p1_example)
full_card_count, full_wins_next = get_count_and_next_wins(full_input)

def update_card_count(card_count, wins_next):
    for i, wins in enumerate(wins_next):
        if wins > 0:
            for k in range(1, card_count[i]+1):
                for j in range(1, wins+1):
                    card_count[i+j] += 1

_ = update_card_count(example_card_count, example_wins_next)
sleep(0.1)
print(f"Total from example: {sum(example_card_count)}")     

_ = update_card_count(full_card_count, full_wins_next)
sleep(0.1)
print(f"Total from full: {sum(full_card_count)}")