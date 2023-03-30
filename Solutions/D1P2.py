# Solve Day 1, Puzzle 2
# https://adventofcode.com/2022/day/1

# D1P1_input.txt provides a list of calories for food items carried by elves
# each food item is on its own line
# each elf's entries are separated by a blank line

# GOAL: How many calories TOTAL are the 3 elves with the most calories carrying?

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

# sort() sorts in ascending order by default
# reverse=True sorts the array in descending order (most calories first)
sorted_calories = calories_per_elf
sorted_calories.sort(reverse=True)

print(sorted_calories[0] + sorted_calories[1] + sorted_calories[2])

################################################################################

# This is the first method I came up with. I ended up going with with the method 
# above because having a list of elves by calorie count makes it easy to find 
# the next highest calorie count (just in case the elves decide they need to
# know more than the top three later on). Also, Python makes sorting easy, so
# why not?

most_cals = 0
second_most_cals = 0
third_most_cals = 0

for elf_cals in calories_per_elf:
    if elf_cals > most_cals:
        third_most_cals = second_most_cals
        second_most_cals = most_cals
        most_cals = elf_cals
    elif elf_cals > second_most_cals:
        third_most_cals = second_most_cals
        second_most_cals = elf_cals
    elif elf_cals > third_most_cals:
        third_most_cals = elf_cals

print(most_cals + second_most_cals + third_most_cals)