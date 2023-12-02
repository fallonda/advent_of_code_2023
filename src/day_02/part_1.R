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

example_full_long <- create_full_long(example_input)

example_results <- example_full_long |>
    pivot_by_colour() |>
    filter_to_allowed_games(
        red_filter = 12,
        green_filter = 13,
        blue_filter = 14
    )

print(sum(unique(example_results$game)))


# Run the full input
full_input <- read_tsv(
    "./src/day_02/full_input.txt",
    show_col_types = FALSE,
    col_names = "text"
)

full_results <- full_input |>
    create_full_long() |>
    pivot_by_colour() |>
    filter_to_allowed_games(
        red_filter = 12,
        green_filter = 13,
        blue_filter = 14
    )

print(sum(unique(full_results$game)))

View(full_results)
