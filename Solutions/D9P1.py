# Solve Day 9, Puzzle 1
# https://adventofcode.com/2022/day/9

# D9P1_input.txt provides a series of movements for a rope. Whenever the Head of
# the rope moves, if it gets far enough away the Tail moves as well.

# GOAL: If a simulated rope moves along a grid as described by the input
# sequence, how many positions will the Tail visit at least once?

################################################################################

class Rope:

    def __init__(self, x_coordinate, y_coordinate):
        self.x = x_coordinate
        self.y = y_coordinate

    def GetCoordinates(self):
        return [self.x, self.y]

################################################################################

# instantiate objects to walk through the sequence
head = Rope(0,0)
tail = Rope(0,0)

# keep track of locations visited by the tail
locations = [[0,0]]

# follow provided movement sequence
input_file = open("../Input/D9.txt")

for line in input_file:

    line_parts = line.split()
    direction = line_parts[0]
    distance = int(line_parts[1].strip())

    i = 0
    while i < distance:

        # move the head first
        if direction == "U":
            head.y += 1
        elif direction == "D":
            head.y -= 1
        elif direction == "L":
            head.x -= 1
        else:
            head.x += 1

        # move the tail next

        # diagonal (up and left)
        if (
            ((head.y - tail.y == 2) and (head.x - tail.x == -1)) or 
            ((head.y - tail.y == 1) and (head.x - tail.x == -2))
        ):
            tail.y += 1
            tail.x -= 1

        # diagonal (up and right)
        elif (
            ((head.y - tail.y == 2) and (head.x - tail.x == 1)) or 
            ((head.y - tail.y == 1) and (head.x - tail.x == 2))
        ):
            tail.y += 1
            tail.x += 1

        # diagonal (down and left)
        elif (
            ((head.y - tail.y == -2) and (head.x - tail.x == -1)) or 
            ((head.y - tail.y == -1) and (head.x - tail.x == -2))
        ):
            tail.y -= 1
            tail.x -= 1

        # diagonal (down and right)
        elif (
            ((head.y - tail.y == -2) and (head.x - tail.x == 1)) or 
            ((head.y - tail.y == -1) and (head.x - tail.x == 2))
        ):
            tail.y -= 1
            tail.x += 1

        # up
        elif (head.y - tail.y == 2):
            tail.y += 1

        # down
        elif (head.y - tail.y == -2):
            tail.y -= 1

        # left
        elif (head.x - tail.x == -2):
            tail.x -= 1

        # right
        elif (head.x - tail.x == 2):
            tail.x += 1

        # tail doesn't move if within 1 unit in any direction from the head

        # add tail position to the list, but only if it isn't already there
        if tail.GetCoordinates() not in locations:
            locations.append(tail.GetCoordinates())

        i += 1

input_file.close()

# # testing...
# print(locations)

# display results
print("Number of Distinct Locations Visited by the Tail:", len(locations))