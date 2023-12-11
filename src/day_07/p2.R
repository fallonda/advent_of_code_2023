library(readr)
library(tidyr)
library(dplyr)
library(forcats)
library(stringr)

read_input <- function(path) {
    read_tsv(
        path,
        col_names = c("hand"),
        show_col_types = FALSE
    ) |>
    separate_wider_delim(hand, delim = " ", names = c("hand", "bid")) |>
    mutate(bid = as.numeric(bid))
}

example <- read_input("./src/day_07/example.txt")
example

# Factors

cards <- factor(
    c("A","K","Q","T","9","8","7","6","5","4","3","2","J"),
    levels = c("A","K","Q","T","9","8","7","6","5","4","3","2","J"),
    ordered = TRUE
)

hands <- factor(
    c(
        "Five of a kind",
        "Four of a kind",
        "Full house",
        "Three of a kind",
        "Two pair",
        "One pair",
        "High card"
    ),
    levels = c(
        "Five of a kind",
        "Four of a kind",
        "Full house",
        "Three of a kind",
        "Two pair",
        "One pair",
        "High card"
    ),
    ordered = TRUE
)

assign_hand <- function(hand) {
    split_hand <- str_split_1(hand, pattern = "")
    if (grepl(x = hand, pattern = "J")) {
        original_freqs <- table(split_hand) |>
            as.data.frame() |> 
            mutate(card = factor(split_hand, levels = cards, ordered = TRUE)) |>
            arrange(Freq, desc(card))
        # Get what J should be.
        new_j <- original_freqs |>
        filter(card != "J") |>
        tail(n=1) |>
        pull(card)
        # Get the new hand with wildcard considered. 
        freqs <- original_freqs |>
            mutate(card = ifelse(card == "J", as.character(new_j), as.character(card))) |>
            group_by(card) |>
            summarise(Freq = sum(Freq)) |>
            ungroup() |>
            arrange(Freq) |>
            mutate(Freq = as.numeric(Freq)) |>
            pull(Freq)
    } else {
        freqs <- table(split_hand) |>
            as.data.frame() |>
            arrange(Freq) |>
            mutate(Freq = as.numeric(Freq)) |>
            pull(Freq)
    }
    
    ret_value <- case_when(
        identical(freqs, 5) ~ "Five of a kind",
        identical(freqs, c(1,4)) ~ "Four of a kind",
        identical(freqs, c(2,3)) ~ "Full house",
        identical(freqs, c(1,1,3)) ~ "Three of a kind",
        identical(freqs, c(1,2,2)) ~ "Two pair",
        identical(freqs, c(1,1,1,2)) ~ "One pair",
        identical(freqs, c(1,1,1,1,1)) ~ "High card",
        .default = "ERROR no hand assigned!"
    )
    return(ret_value)
}

# tests
# assign_hand("AAAAA")
# assign_hand("AAAAJ")
# assign_hand("AAAAQ")
# assign_hand("AAAJK")
# assign_hand("AAAKK")
# assign_hand("AAAKQ")
# assign_hand("AAJKQ")
# assign_hand("AAKKQ")
# assign_hand("A3QQJ")
# assign_hand("AAKQT")
# assign_hand("AKQT9")
# assign_hand("AKQTJ")
# assign_hand("KTJJT")
# assign_hand("J57J8")

calc_winnings <- function(input) {
    calc_df <- input |>
        separate_wider_position(hand, widths = c(
            "card_1" = 1,
            "card_2" = 1,
            "card_3" = 1,
            "card_4" = 1,
            "card_5" = 1
        ),
        cols_remove = FALSE) |>
        rowwise() |>
        mutate(hand_called = assign_hand(hand)) |>
        ungroup() |>
        mutate(
            hand_called = factor(hand_called, levels = hands, ordered = TRUE),
            card_1 = factor(card_1, levels = cards, ordered = TRUE),
            card_2 = factor(card_2, levels = cards, ordered = TRUE),
            card_3 = factor(card_3, levels = cards, ordered = TRUE),
            card_4 = factor(card_4, levels = cards, ordered = TRUE),
            card_5 = factor(card_5, levels = cards, ordered = TRUE)
        ) |>
        arrange(
            desc(hand_called),
            desc(card_1),
            desc(card_2),
            desc(card_3),
            desc(card_4),
            desc(card_5)
        ) |>
        mutate(rank = row_number()) |>
        mutate(winnings = rank * bid)
    return(calc_df)
}

# Example
calc_winnings(example)
sum(calc_winnings(example)$winnings)

# Full input
full_input <- read_input("./src/day_07/full_input.txt")
results_df <- calc_winnings(full_input)
sum(results_df$winnings)
# View(results_df |> filter(grepl("J", hand)))
