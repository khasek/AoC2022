# Solve Day 6, Puzzle 1
# https://adventofcode.com/2022/day/6

# D6P1_input.txt provides a string of seemingly-random characters that represent
# a communication signal. The transmission starts with a buffer, and the actual
# message begins after a start-of-packet marker (in this case, 4 unique
# characters in a row). 

# GOAL: How many characters have to be processed before the end of the
# start-of-packet marker? (i.e. What is the index of the first character of the
# packet?)

################################################################################

input_file = open("../Input/D6.txt")

# text in file is all on one line
transmission = input_file.readline()

input_file.close()



# this will be the index of the first character after the start-of-packet marker
# at minimum, 4 characters will need to process (assuming the marker appears right away)
target_index = 4

# examine a window of 4 characters at a time

short_string = [transmission[0], transmission[1], 
                transmission[2], transmission[3]]

transmission_length = len(transmission)
while target_index < (transmission_length):

    # if there are repeat characters, move the window forward by 1
    if len(short_string) != len(set(short_string)):
        short_string.pop(0)
        short_string.append(transmission[target_index])
        target_index += 1

    # if there are no repeat characters, we've found the right index
    else:
        print("Packet begins after", target_index, "characters")
        break



# if the loop above cycles all the way through, check whether the last 4
# characters form a marker
if target_index == transmission_length:
    
    if len(short_string) == len(set(short_string)):
        print("Marker found after", target_index, 
              "characters, but no packet followed")
    else:
        print("No marker found")

