# Solve Day 9, Puzzle 2
# https://adventofcode.com/2022/day/9

# D9P1_input.txt provides a series of movements for a rope. This time, the rope
# is 10 knots long (head plus 1-9). When the knot in front of any particular
# knot gets far enough away, that knot moves as described previously.

# GOAL: If a simulated rope of 10 knots moves along a grid as described by the 
# input sequence, how many positions will the Tail visit at least once?

# Notes: First answer of 373 was too low. Turns out I had neglected to account
# for the fact that a leading node might move diagonally, which slightly changed
# the possible differences in position between one node and the next.

################################################################################

class Knot:

    def __init__(self, x_coordinate, y_coordinate):
        self.x = x_coordinate
        self.y = y_coordinate

    def GetCoordinates(self):
        return [self.x, self.y]

################################################################################

# instantiate objects to walk through the sequence

# head will be index 0, tail will be index -1
rope = []

number_of_knots = 10
i = 0

while i < number_of_knots:
    rope.append(Knot(0,0))
    i += 1

# keep track of locations visited by the tail
locations = [[0,0]]

# follow provided movement sequence
input_file = open("../Input/D9.txt")

for line in input_file:

    line_parts = line.split()
    direction = line_parts[0]
    distance = int(line_parts[1].strip())

    distance_iter = 0
    while distance_iter < distance:

        # move the head first
        if direction == "U":
            rope[0].y += 1
        elif direction == "D":
            rope[0].y -= 1
        elif direction == "L":
            rope[0].x -= 1
        else:
            rope[0].x += 1

        # move rest of the knots one at a time
        knot_iter = 1
        while knot_iter < number_of_knots:

            current = rope[knot_iter]
            previous = rope[knot_iter - 1]

            # diagonal (up and left)
            if (
                ((previous.y - current.y == 2) and (previous.x - current.x <= -1)) or 
                ((previous.y - current.y >= 1) and (previous.x - current.x == -2))
            ):
                current.y += 1
                current.x -= 1

            # diagonal (up and right)
            elif (
                ((previous.y - current.y == 2) and (previous.x - current.x >= 1)) or 
                ((previous.y - current.y >= 1) and (previous.x - current.x == 2))
            ):
                current.y += 1
                current.x += 1

            # diagonal (down and left)
            elif (
                ((previous.y - current.y == -2) and (previous.x - current.x <= -1)) or 
                ((previous.y - current.y <= -1) and (previous.x - current.x == -2))
            ):
                current.y -= 1
                current.x -= 1

            # diagonal (down and right)
            elif (
                ((previous.y - current.y == -2) and (previous.x - current.x >= 1)) or 
                ((previous.y - current.y <= -1) and (previous.x - current.x == 2))
            ):
                current.y -= 1
                current.x += 1

            # up
            elif (previous.y - current.y == 2):
                current.y += 1

            # down
            elif (previous.y - current.y == -2):
                current.y -= 1

            # left
            elif (previous.x - current.x == -2):
                current.x -= 1

            # right
            elif (previous.x - current.x == 2):
                current.x += 1

            # knot doesn't move if within 1 unit in any direction from previous knot
            # if one knot doesn't move, subsequent knots won't move
            else:
                break

            knot_iter += 1

        # add tail position to the list if it isn't already there
        tail_coordinates = rope[-1].GetCoordinates()

        if tail_coordinates not in locations:
            locations.append(tail_coordinates)

        distance_iter += 1

input_file.close()

# # testing...
# print(locations)

# display results
print("Number of Distinct Locations Visited by the Tail:", len(locations))