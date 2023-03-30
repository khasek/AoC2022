# Solve Day 10, Puzzle 1
# https://adventofcode.com/2022/day/10

# D10P1_input.txt provides a series of signals sent to your com device's screen
# by the CPU. Each line is a cycle; the "noop" command takes one cycle and does
# nothing, while an "addx" command takes two cycles and changes the value X of 
# the register. Signal strength is calculated by multiplying the cycle number by
# the value of register X.

# GOAL: Find the signal strength DURING cycles 20, 60, 100, 140, 180, and 220. 
# Submit the sum of those signal strengths.

# Notes: My first answer (7840) was too low. I had used each line as a cycle
# (and "addx" commands took 2 lines to process), but the program should pause 
# for an extra cycle on each "addx" command. Got it on my second attempt!

################################################################################

# value of the register; starts at 1
register = 1

# these are the cycles during which signal strength should be checked
designated_cycles = [20, 60, 100, 140, 180, 220]

# use to keep track of signal strength during the designated cycles
signal_strengths = []



# process puzzle input
input_file = open("../Input/D10.txt")

cycle_num = 0
for line in input_file:

    # increment cycle and check whether signal strength should be recorded
    cycle_num += 1
    if cycle_num in designated_cycles:
        signal_strengths.append(cycle_num * register)

    # if command is "noop", nothing else needs to be done
    # if command is "addx", increment cycle again and update register
    if line.strip() != "noop":

        cycle_num += 1
        if cycle_num in designated_cycles:
            signal_strengths.append(cycle_num * register)

        line_parts = line.split()
        register_change = int(line_parts[1].strip())
        register += register_change
        # print(register)

input_file.close()



# display sum of signal strengths
signal_sum = 0
for ss in signal_strengths:
    print(ss)
    signal_sum += ss

print("\nSignal Sum:", signal_sum)