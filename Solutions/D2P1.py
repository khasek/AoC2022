# Solve Day 2, Puzzle 1
# https://adventofcode.com/2022/day/2

# D2P1_input.txt provides a set of strategic moves for the upcoming
# rock-paper-scissors tournament. Points are calculated as follows:

# Rock      (A/X)   1
# Paper     (B/Y)   2
# Scissors  (C/Z)   3

# Win               6
# Lose              0
# Draw              3

# GOAL: How many points will you earn if the strategy guide is accurate and you
# choose to follow it?

# Notes: First implementation was incorrect (my solution of 17366 was too high).
# Turns out when I parsed each line, the newline character was included as part
# of my move and my program interpreted that move as "scissors". Fixed the
# problem by only examining the first character of matchup[1].

################################################################################

input_file = open("../Input/D2.txt")

total_points = 0

for line in input_file:

    # parse the line so we know which move each person made
    # the opponent's move will be at index 0, and yours will be index 1
    matchup = line.split(" ")

    # calculate points
    # points for choosing "rock"
    if matchup[1][0] == "X":

        total_points += 1

        # points for a win
        if matchup[0] == "C":
            total_points += 6

        # points for a draw
        elif matchup[0] == "A":
            total_points += 3

    # points for choosing "paper"
    elif matchup[1][0] == "Y":

        total_points += 2

        # points for a win
        if matchup[0] == "A":
            total_points += 6

        # points for a draw
        elif matchup[0] == "B":
            total_points += 3

    # points for choosing "scissors"
    else:

        total_points += 3

        # points for a win
        if matchup[0] == "B":
            total_points += 6

        # points for a draw
        elif matchup[0] == "C":
            total_points += 3

input_file.close()

print(total_points)