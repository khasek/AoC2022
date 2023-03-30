# Solve Day 13, Puzzle 1
# https://adventofcode.com/2022/day/13

# D13P1_input.txt provides a list of paired signal packets, some of which are
# in the wrong order. Lower numbers should come before higher numbers, and 
# shorter lists should come before longer ones.

# GOAL: Find the indices of pairs that are in the right order (STARTS AT 1). 
# Submit the sum of those indices.

# Notes: After parsing my input strings the hard way, I learned about Python's
# eval() function. SUPER HANDY FUNCTION. I'm noting it here for future
# reference.

################################################################################

# Returns a list with two items: 0) a list parsed from the provided string, and 
# 1) the number of characters that have been processed. Assumes input string 
# starts with "[" and end with "]".
def StringToList(input_string, current_index):

    integers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    max_index = len(input_string)

    int_string = ""
    current_list = []

    while current_index < max_index:

        char = input_string[current_index]

        if char in integers:
            int_string += char
        elif char == ",":
            if int_string != "":
                current_list.append(int(int_string))
                int_string = ""
        elif char == "[":
            recursion_results = StringToList(input_string, current_index + 1)
            current_list.append(recursion_results[0])
            current_index = recursion_results[1]
        elif char == "]":
            if int_string != "":
                current_list.append(int(int_string))
                int_string = ""
            return [current_list, current_index]

        current_index += 1

    return [current_list, current_index]



# Compares two lists item by item, checking for correct order. Returns True if
# list1 should be ordered before list2; otherwise returns False.
def CompareLists(list1, list2):

    # find the length of the shorter list (so we know when to stop comparing)
    length1 = len(list1)
    length2 = len(list2)

    if length1 <= length2:
        short_length = length1
    else:
        short_length = length2

    # iterate through list items until order correctness can be determined, 
    # or until we've iterated all the way through the shorter list
    i = 0
    while i < short_length:

        item1 = list1[i]
        item2 = list2[i]

        # if both items are ints, the smaller int should be listed first
        if (
            (type(item1) == int) and 
            (type(item2) == int)
        ):
            if item1 < item2:
                return True
            elif item1 > item2:
                return False

        # if both items are lists (and they aren't the same list), 
        # compare each sublist item by item
        elif (
            (type(item1) == list) and 
            (type(item2) == list) and 
            (item1 != item2)
        ):
            return CompareLists(item1, item2)

        # if one item is a list and the other is an int, convert the int to a 
        # list and compare both items as lists
        elif (
            ((type(item1) == list) and (type(item2) == int)) or
            ((type(item1) == int) and (type(item2) == list))
        ):
            if type(item1) == int:
                item1 = [item1]
            elif type(item2) == int:
                item2 = [item2]
            
            if item1 != item2:
                return CompareLists(item1, item2)

        i += 1

    # If the above loop finished and no values were returned, the contents of 
    # the two lists must be the same for the first short_length characters. That
    # being the case, the shorter list should come first.
    if length1 <= length2:
        return True
    else:
        return False

################################################################################

# use the puzzle input to create a list of signal packet pairs
packet_pairs = [[]]

input_file = open("../Input/D13.txt")

for line in input_file:

    if line != "\n":

        # StringToList returns an extra level of list, so I added a second
        # index reference ("[0]")
        list_from_line = StringToList(line, 0)[0][0]

        if len(packet_pairs[-1]) < 2:
            packet_pairs[-1].append(list_from_line)
        else:
            new_pair = [list_from_line]
            packet_pairs.append(new_pair)

input_file.close()



# use this list to store a bool for each pair in packet_pairs
# store True if the pair is ordered correctly, or False if it isn't
pair_orders = []
for pair in packet_pairs:
    pair_orders.append(CompareLists(pair[0], pair[1]))

# add indices of correctly ordered pairs
# according to puzzle instructions, indices should start at 1
index_sum = 0
current_index = 1

for val in pair_orders:

    if val:
        index_sum += current_index

    current_index += 1

# display results
print(index_sum)
