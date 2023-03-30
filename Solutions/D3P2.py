# Solve Day 3, Puzzle 2
# https://adventofcode.com/2022/day/3

# D3P1_input.txt provides a list of items (by type) in each elven rucksack.
# Elves are divided into groups of three, so every three lines represents a
# group. Within a group of elves, exactly one item type should be carried by all
# three elves; this will be the type of their group's badge.

# GOAL: Find the item type for each group's badge. Add the priority levels for
# each group's badges and submit the total.

# Priority levels are as follows:
# a-z = 1-26
# A-Z = 27-52

################################################################################

# Instead of storing priority levels for different characters, I used their 
# ASCII values. ASCII values start at 97 for lowercase letters, and 65 for
# uppercase.

def CalculatePriority(letter):
    if letter.isupper():
        return ord(letter) - 38
    else:
        return ord(letter) - 96

################################################################################

input_file = open("../Input/D3.txt")

badges = []

total_elves = 300
total_groups = 100

# Compare rucksack contents one group at a time
group_num = 1
while group_num <= total_groups:

    elf1 = input_file.readline().strip()
    elf2 = input_file.readline().strip()
    elf3 = input_file.readline().strip()

    # Check each type of item in the first elf's rucksack.
    for char in elf1:

        # Is that item type in the second elf's rucksack?
        if char in elf2:

            # If yes, is that item type also in the third elf's rucksack?
            if char in elf3:

                # If yes, this item type must be the badge.
                badges.append(char)
                print(group_num, ":", char)
                break

    group_num += 1

input_file.close()

# Tally priority levels
total_priority = 0
for badge in badges:
    total_priority += CalculatePriority(badge)

print("\nTotal Priority:", total_priority)