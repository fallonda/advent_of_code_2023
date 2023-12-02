import re
from src.utils import read_text

# Read in files
example_input = read_text("./src/day_01/example.txt")
full_input = read_text("./src/day_01/full_input.txt")
    


def get_results(input):
    results_list = []
    regex_pattern = r"[0-9]"
    for j in input:
        all_matches = re.findall(regex_pattern, j)
        first_value = str(all_matches[0])
        second_value = str(all_matches[-1])
        combined_value = "".join([first_value, second_value])
        results_list.append(int(combined_value))
    
    summed_value = sum(results_list)
    return(results_list, summed_value)

get_results(example_input)

get_results(full_input)

