# Solve Day 10, Puzzle 2
# https://adventofcode.com/2022/day/10

# D10P1_input.txt provides a series of signals sent to your com device's screen
# by the CPU. Each line is a cycle; the "noop" command takes one cycle and does
# nothing, while an "addx" command takes two cycles and changes the value X of 
# the register. 
#
# Register X apparently controls the horizontal position of a sprite (more 
# specifically, the sprite is 3 pixels wide and X is the horizontal position of
# the middle pixel). The CRT screen is 40px wide by 6px tall, and it draws a 
# single pixel each cycle (left to right, top to bottom, 240 total 
# pixels/cycles). If any part of the sprite is located on a pixel during the 
# cycle on which that pixel is drawn, the pixel will be lit (#). Otherwise, the
# pixel will be left dark (.).

# GOAL: Render the image given by the input program. Eight capital letters
# should appear.

################################################################################

# determined by the value of the register
# starts at 1; possible values are between -1 and 39 (used Part 1 to check)
sprite_position = 1

# "#" for lit pixels, "." for unlit pixels
drawn_pixels = []



# process puzzle input
input_file = open("../Input/D10.txt")

cycle_num = 0
for line in input_file:

    # increment cycle and draw a pixel
    cycle_num += 1
    horizontal_pixel_position = (cycle_num - 1) % 40

    if abs(sprite_position - horizontal_pixel_position) <= 1:
        drawn_pixels.append("#")
    else:
        drawn_pixels.append(".")


    # if command is "noop", nothing else needs to be done
    # if command is "addx", increment cycle again and update register
    if line.strip() != "noop":

        cycle_num += 1
        horizontal_pixel_position = (cycle_num - 1) % 40

        if abs(sprite_position - horizontal_pixel_position) <= 1:
            drawn_pixels.append("#")
        else:
            drawn_pixels.append(".")

        line_parts = line.split()
        register_change = int(line_parts[1].strip())
        sprite_position += register_change

input_file.close()



# write 240 pixels to an output file for easy viewing
# add a line break after every 40px
output = open("D10P2.txt", "a")
i = 0

while i < 40:
    output.write(drawn_pixels[i])
    i += 1

output.write("\n")

while i < 80:
    output.write(drawn_pixels[i])
    i += 1

output.write("\n")

while i < 120:
    output.write(drawn_pixels[i])
    i += 1

output.write("\n")

while i < 160:
    output.write(drawn_pixels[i])
    i += 1

output.write("\n")

while i < 200:
    output.write(drawn_pixels[i])
    i += 1

output.write("\n")

while i < 240:
    output.write(drawn_pixels[i])
    i += 1

output.close()
