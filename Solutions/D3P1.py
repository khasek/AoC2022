# Solve Day 3, Puzzle 1
# https://adventofcode.com/2022/day/3

# D3P1_input.txt provides a list of items (by type) in each elven rucksack. The
# first half of each line represents items in the first compartment, and the 
# second half represents items in the second compartment. Each item type should
# only appear in one compartment per rucksack, but the elf in charge made a 
# mistake; now there's exactly one item type per rucksack that has been
# erroneously distributed into both compartments.

# GOAL: Find the incorrectly-distributed item type for each rucksack. Add the 
# priority levels for these items together, and submit the total.

# Priority levels are as follows:
# a-z = 1-26
# A-Z = 27-52

# Notes: My first implementation was incorrect (my solution of 7945 was too
# low). On checking, 12 satchels did not list a misplaced item. Changing the 
# midline so that rucksacks with an odd number of items put the extra item in 
# their second compartment fixed this error.

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



# CREATE A LIST OF ITEMS THAT WERE STORED INCORRECTLY

misplaced_items = []

for line in input_file:

    # divide the line in half

    # Satchels with an odd number of items must put the extra in compartment 2;
    # my first implementation put the extras in compartment 1, and there were 12
    # rucksacks without a misplaced item.

    first_half = []
    second_half = [] # includes newline characters

    line_length = len(line)
    midline = (line_length / 2) - 1

    char_index = 0
    while char_index <= midline:
        first_half.append(line[char_index])
        char_index += 1

    while char_index < line_length:
        second_half.append(line[char_index])
        char_index += 1
    
    # compare the halves for shared characters
    # since there should be exactly one, we can stop comparing after we find it
    for char in first_half:
        if char in second_half:
            misplaced_items.append(char)
            break

input_file.close()



# CALCULATE TOTAL PRIORITY

total_priority = 0

for item in misplaced_items:
    total_priority += CalculatePriority(item)

print(len(misplaced_items))
print(total_priority)