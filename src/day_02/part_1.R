library(readr)
library(dplyr)
library(tidyr)

example_input <- read_tsv(
    "./src/day_02/part_1_example.txt",
    show_col_types = FALSE,
    col_names = "text"
)

example_full_long <- example_input |>
separate_wider_delim(
    cols = text,
    delim = ": ",
    names = c("text", "samples")
) |>
separate_longer_delim(
    cols = samples,
    delim = "; ",
) |>
group_by(text) |>
mutate(sampling = row_number()) |>
ungroup() |>
separate_longer_delim(
    cols = samples,
    delim = ", "
) |>
separate_wider_delim(
    cols = samples,
    delim = " ",
    names = c("number", "colour")
) |>
rename(game = text) |>
mutate(game = gsub(
    pattern = "Game ",
    replacement = "",
    x = game
)) |>
mutate(
    number = as.numeric(number),
    game = as.numeric(game)
)

example_piv_by_colour <- example_full_long |>
pivot_wider(
    id_cols = c("game", "sampling"),
    names_from = colour,
    values_from = number
) |>
replace_na(list(
    blue = 0,
    red = 0,
    green = 0
))

allowed_games <- example_piv_by_colour |>
mutate(
    sampling_allowed = {
        (blue <= 14) &
        (red <= 12) &
        (green <= 13)
    }
) |>
group_by(game) |>
mutate(
    game_allowed = all(sampling_allowed)
) |>
ungroup() |>
filter(game_allowed)

sum(unique(allowed_games$game))
