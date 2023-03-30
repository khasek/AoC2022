# Solve Day 4, Puzzle 2
# https://adventofcode.com/2022/day/4

# D4P1_input.txt provides a list of section assignments. Each line has two
# section ranges. (ex: 24-91,80-92)

# GOAL: For how many pairs does one range overlap the other at all?

################################################################################

input_file = open("../Input/D4.txt")

overlap_count = 0

for line in input_file:

    # separate pairs
    assignment_pair = line.split(",")

    assignment1 = assignment_pair[0].split("-")
    assignment2 = assignment_pair[1].split("-")

    # find min and max for each range
    min1 = int(assignment1[0])
    max1 = int(assignment1[1])

    min2 = int(assignment2[0])
    max2 = int(assignment2[1].strip())

    # compare and increment the number of complete overlaps as needed

    if (min1 > min2) and (min1 <= max2):
        overlap_count += 1
    elif (min2 > min1) and (min2 <= max1):
        overlap_count += 1
    elif (min1 == min2):
        overlap_count += 1

input_file.close()

print("Number of Overlaps:", overlap_count)

