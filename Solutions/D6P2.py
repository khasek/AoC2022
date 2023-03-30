# Solve Day 6, Puzzle 2
# https://adventofcode.com/2022/day/6

# D6P1_input.txt provides a string of seemingly-random characters that represent
# a communication signal. The transmission will contain start-of-packet markers 
# (4 unique characters in a row), as well as start-of-message markers (14 unique
# characters in a row). 

# GOAL: How many characters have to be processed before the end of the
# start-of-message marker? (i.e. What is the index of the first character of the
# message?)

################################################################################

input_file = open("../Input/D6.txt")

# text in file is all on one line
transmission = input_file.readline()

input_file.close()



# at minimum, 14 characters will need to process (assuming the marker appears right away)
marker_length = 14

# this will be the index of the first character after the start-of-packet marker
target_index = marker_length



# create a window of 14 characters
short_string = []
i = 0
while i < marker_length:
    short_string.append(transmission[i])
    i += 1

# examine 14 characters at a time
transmission_length = len(transmission)
while target_index < (transmission_length):

    # if there are repeat characters, move the window forward by 1
    if len(short_string) != len(set(short_string)):
        short_string.pop(0)
        short_string.append(transmission[target_index])
        target_index += 1

    # if there are no repeat characters, we've found the right index
    else:
        print("Message begins after", target_index, "characters")
        break



# if the loop above cycles all the way through, check whether the last 14
# characters form a marker
if target_index == transmission_length:
    
    if len(short_string) == len(set(short_string)):
        print("Marker found after", target_index, 
              "characters, but no message followed")
    else:
        print("No marker found")

