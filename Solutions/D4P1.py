# Solve Day 4, Puzzle 1
# https://adventofcode.com/2022/day/4

# D4P1_input.txt provides a list of section assignments. Each line has two
# section ranges. (ex: 24-91,80-92)

# GOAL: For how many pairs does one range completely overlap the other?

# Notes: My first guess of 507 is too low. Checking to make sure my input is
# correct before trying again. UPDATE: Input was correct. The problem was that
# newline character again -- I'm going to have to remember to remove that every
# time, whether or not I think it makes a difference. On the bright side, I 
# learned that in Python a string with a number ("42") is considered less than
# a string with the same number plus a newline ("42\n"). UPDATE: My second
# guess of 569 was too high? Ah, I neglected to convert my strings to ints,
# which had the result of incorrectly comparing numbers with a different number
# of digits (i.e. "2" would have been greater than "10").

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

    if (min1 > min2) and (max1 <= max2):
        overlap_count += 1
    elif (min1 < min2) and (max1 >= max2):
        overlap_count += 1
    elif (min1 == min2):
        overlap_count += 1

input_file.close()

print("Number of Complete Overlaps:", overlap_count)

