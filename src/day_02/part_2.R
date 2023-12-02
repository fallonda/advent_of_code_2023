library(readr)
library(dplyr)
library(tidyr)

source("./src/day_02/functions.R")

# Run the example: 
example_input <- read_tsv(
    "./src/day_02/part_1_example.txt",
    show_col_types = FALSE,
    col_names = "text"
)

pt2_example_results <- example_input |>
    create_full_long() |>
    get_min_dice() |>
    get_power() |>
    get_sum()

print(pt2_example_results)


# Run the full input
full_input <- read_tsv(
    "./src/day_02/full_input.txt",
    show_col_types = FALSE,
    col_names = "text"
)

pt2_full_results <- full_input |>
    create_full_long() |>
    get_min_dice() |>
    get_power() |>
    get_sum()

print(pt2_full_results)



