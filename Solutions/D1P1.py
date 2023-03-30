# Solve Day 1, Puzzle 1
# https://adventofcode.com/2022/day/1

# D1P1_input.txt provides a list of calories for food items carried by elves
# each food item is on its own line
# each elf's entries are separated by a blank line

# GOAL: How many calories is the elf with the most calories carrying?

################################################################################

input_file = open("../Input/D1.txt")

calories = 0
calories_per_elf = []

for line in input_file:
    if line == "\n":
        calories_per_elf.append(calories)
        calories = 0
    else:
        calories += int(line)

input_file.close()

print(max(calories_per_elf))