# Solve Day 5, Puzzle 1
# https://adventofcode.com/2022/day/5

# D5P1_input.txt provides an image that represents 9 stacks of labelled crates.
# It also provides instructions for the elves' crane operator to move crates
# between stacks (one at a time). 

# GOAL: Which crate ends up on top of each stack? Answer should be submitted as
# a 9-character string.

################################################################################

# parameters 2 and 3 are indices in the "crates" list
def MoveCrates(num_moved, from_stack, to_stack):
    iter = 0
    while iter < num_moved:
        crates[to_stack].append(crates[from_stack].pop())
        iter += 1

################################################################################

# stacks of crates; the end of the list is the top of the stack
stack1 = ["B", "P", "N", "Q", "H", "D", "R", "T"]
stack2 = ["W", "G", "B", "J", "T", "V"]
stack3 = ["N", "R", "H", "D", "S", "V", "M", "Q"]
stack4 = ["P", "Z", "N", "M", "C"]
stack5 = ["D", "Z", "B"]
stack6 = ["V", "C", "W", "Z"]
stack7 = ["G", "Z", "N", "C", "V", "Q", "L", "S"]
stack8 = ["L", "G", "J", "M", "D", "N", "V"]
stack9 = ["T", "P", "M", "F", "Z", "C", "G"]

crates = [stack1, stack2, stack3, stack4, stack5, 
          stack6, stack7, stack8, stack9]

# move crates
input_file = open("../Input/D5.txt")

for line in input_file:

    # all lines are in the format "move x from y to z"
    words = line.split(" ")
    crates_moved = int(words[1])

    # subtract 1 for index
    move_from = int(words[3]) - 1
    move_to = int(words[5].strip()) - 1

    MoveCrates(crates_moved, move_from, move_to)

input_file.close()

# display top crate from each stack
output_string = ""
for stack in crates:
    print(stack)
    output_string += str(stack[-1])

print(output_string)