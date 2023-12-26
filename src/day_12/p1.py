from src.utils import read_text

example = read_text("./src/day_12/example.txt")

lines = [x.split("\n")[0] for x in example]
cyph_and_nums = [(x.split(" ")[0], x.split(" ")[1]) for x in lines]

combs = 0
for cyph, nums in cyph_and_nums:
    for x in cyph:
        if x == "."