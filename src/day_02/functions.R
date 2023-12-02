
create_full_long <- function(df) {
    full_long <- df |>
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
return(full_long)
}

pivot_by_colour <- function(df) {
    piv_by_colour <- df |>
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
return(piv_by_colour)
}

filter_to_allowed_games <- function(df, red_filter, green_filter, blue_filter) {
    allowed_games <- df |>
mutate(
    sampling_allowed = {
        (blue <= blue_filter) &
        (red <= red_filter) &
        (green <= green_filter)
    }
) |>
group_by(game) |>
mutate(
    game_allowed = all(sampling_allowed)
) |>
ungroup() |>
filter(game_allowed)
return(allowed_games)
}


get_min_dice <- function(df) {
    df |> 
    group_by(game, colour) |>
    slice_max(number, with_ties = FALSE)
}

get_power <- function(df) {
    df |>
    group_by(game) |>
    summarise(pwr = prod(number)) |>
    ungroup()
}

get_sum <- function(df) {
    value <- sum(df$pwr)
    return(value)
}
