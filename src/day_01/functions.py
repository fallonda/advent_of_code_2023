def convert_string_to_number(input):
    """Convert number as a string e.g. 'eight'
    to a digit e.g. 8."""
    string_numbers = [
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine"
    ]
    if input in string_numbers:
        number = string_numbers.index(input)+1
    else:
        number = input
    return number