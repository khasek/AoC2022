# Solve Day 2, Puzzle 2
# https://adventofcode.com/2022/day/2

# D2P1_input.txt provides a set of strategic moves for the upcoming
# rock-paper-scissors tournament. Unfortunately, we interpreted the guide wrong
# before; the second column actually describes whether we need to win, lose, or
# draw for that round. Points are calculated as follows:

# Rock      (A)   1
# Paper     (B)   2
# Scissors  (C)   3

# Win       (Z)   6
# Draw      (Y)   3
# Lose      (X)   0

# GOAL: How many points will you earn if the strategy guide is accurate and you
# choose to follow it?

################################################################################

input_file = open("../Input/D2.txt")

total_points = 0

for line in input_file:

    # parse the line so we know which move each person made
    # the opponent's move will be at index 0, and your outcome will be index 1
    matchup = line.split(" ")

    # calculate points
    # opponent chooses "rock"
    if matchup[0] == "A":

        # points for a win
        if matchup[1][0] == "Z":
            # 6 for win + 2 for paper
            total_points += 8

        # points for a draw
        elif matchup[1][0] == "Y":
            # 3 for draw + 1 for rock
            total_points += 4

        # points for a loss
        else:
            # 0 for loss + 3 for scissors
            total_points += 3

    # opponent chooses "paper"
    elif matchup[0] == "B":

        # points for a win
        if matchup[1][0] == "Z":
            # 6 for win + 3 for scissors
            total_points += 9

        # points for a draw
        elif matchup[1][0] == "Y":
            # 3 for draw + 2 for paper
            total_points += 5

        # points for a loss
        else:
            # 0 for loss + 1 for rock
            total_points += 1

    # opponent chooses "scissors"
    else:

        # points for a win
        if matchup[1][0] == "Z":
            # 6 for win + 1 for rock
            total_points += 7

        # points for a draw
        elif matchup[1][0] == "Y":
            # 3 for draw + 3 for scissors
            total_points += 6

        # points for a loss
        else:
            # 0 for loss + 2 for paper
            total_points += 2

input_file.close()

print(total_points)

