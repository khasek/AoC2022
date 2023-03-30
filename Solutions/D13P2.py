# Solve Day 13, Puzzle 2
# https://adventofcode.com/2022/day/13

# D13P1_input.txt provides a list of paired signal packets, some of which are
# in the wrong order. Lower numbers should come before higher numbers, and 
# shorter lists should come before longer ones.

# GOAL: Add two divider packets ([[2]] and [[6]]), then rearrange ALL the 
# packets to be in the correct order. Find the indices of the divider packets 
# and multiply them together (again, indices start at 1). Submit this product 
# (the decoder key).

# Notes: My first answer was too low. Whoops, forgot to change the indices so
# they started at 1 instead of 0. Easy fix.

################################################################################

# Compares two lists item by item, checking for correct order. Returns True if
# list1 should be ordered before list2; otherwise returns False.
def ComparePackets(list1, list2):

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
            return ComparePackets(item1, item2)

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
                return ComparePackets(item1, item2)

        i += 1

    # If the above loop finished and no values were returned, the contents of 
    # the two lists must be the same for the first short_length characters. That
    # being the case, the shorter list should come first.
    if length1 <= length2:
        return True
    else:
        return False

################################################################################

# use the puzzle input to create a list of signal packets
# add the two divider packets first (in order)
packets = [[[2]], [[6]]]

input_file = open("../Input/D13.txt")

# as each additional packet is added, make sure it gets placed so the 
# packet list remains sorted
for line in input_file:

    if line != "\n":

        # evaluate from a string to lists and ints
        new_packet = eval(line)

        # find the index of the first list item that should be ordered after the
        # current packet; insert new packet at that index
        current_length = len(packets)
        i = 0

        while (i < current_length) and ComparePackets(packets[i], new_packet):
            i += 1

        packets.insert(i, new_packet)

input_file.close()

# testing...
# print(packets[0])
# print(packets[-1])



# find updated indices of the divider packets
# packet indices should start at 1 instead of 0
divider_index_1 = packets.index([[2]]) + 1
divider_index_2 = packets.index([[6]]) + 1

# display the decoder key (product of divider indices)
print("Decoder key:", divider_index_1 * divider_index_2)