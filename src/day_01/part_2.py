import re
from src.utils import read_text
from src.day_01.functions import convert_string_to_number

# Read in files
part_2_example_input = read_text("./src/day_01/part_2_example.txt")
full_input = read_text("./src/day_01/full_input.txt")
    
def parse_for_value(string):
    regex_to_search = [
        r"[0-9]",
        r"one",
        r"two",
        r"three",
        r"four",
        r"five",
        r"six",
        f"seven",
        f"eight",
        f"nine"
    ]
    match_dict = {}
    for pattern in regex_to_search:
        match = re.finditer(
            pattern = pattern,
            string = string
        )
        for i in match:
            if (i is not None):
                match_dict[i.start()] = i.group()
    # Sort the dictionary
    sorted_dict = dict(sorted(match_dict.items()))
    return(sorted_dict)

# e.g.         
# parse_for_value("oneeightwone")

def get_first_last_value(sorted_dict: dict) -> tuple:
    values = list(sorted_dict.values())
    first_value = convert_string_to_number(values[0])
    last_value = convert_string_to_number(values[-1])
    return (str(first_value), str(last_value))

# e.g.  
# get_first_last_value(
#     parse_for_value("oneeightwone")
# )
    
def get_results_pt2(input):
    results_list = []
    for j in input:
        all_matches = parse_for_value(j)
        first_and_last_match = get_first_last_value(all_matches)
        combined_value = "".join(first_and_last_match)
        results_list.append(int(combined_value))
    
    summed_value = sum(results_list)
    return(results_list, summed_value)

get_results_pt2(part_2_example_input)

get_results_pt2(full_input)

get_results_pt2(["oneightwoone"])