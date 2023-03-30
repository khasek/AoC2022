# Solve Day 14, Puzzle 2
# https://adventofcode.com/2022/day/14

# D14P1_input.txt provides a scan of rock formations in a cave, represented as 
# lines drawn between coordinates on a 2D grid. Sand is falling from the roof at
# point (500,0). Sand falls one unit at a time, with the next unit falling once
# the first has come to rest. Sand attempts to fall directly down; if the next
# point down is blocked, it attempts to move first diagonally down and left, 
# then diagonally down and right. If all three directions are blocked, the unit
# of sand comes to a rest and the next unit begins to fall. FOR PART 2, there is
# now a floor 2 units below the lowest rock structure. For our purposes, the 
# floor is completely flat and extends infinitely far in each horizontal 
# direction.

# GOAL: Simulate the falling sand. How many units of sand come to rest on the 
# rock formations before the source is blocked?

# Note: My first answer (25559) was too high. Turns out I'd forgotten to change 
# the fill status the floor Points. My second answer (25247) was too low. I 
# needed to account for the last unit of sand (the one that blocked the source).
# My third answer (25248) was correct.

################################################################################

# describes a point in space
# stores 2D coordinates and fill status (False for air, True for rock/sand)
class Point:
    
    def __init__(self, x_int, y_int):
        self.x = x_int
        self.y = y_int
        self.filled = False



# takes two points that are aligned vertically or horizontally on a grid
# changes filled val to True for all points between the two provided (inclusive)
def FillRockLine(point_grid, point1, point2):

    # vertical line
    if point1.x == point2.x:

        # line start and stop y vals
        if point1.y < point2.y:
            min_row = point1.y
            max_row = point2.y
        else:
            min_row = point2.y
            max_row = point1.y
        
        column = point1.x
        current_row = min_row

        # fill each Point in the line
        while current_row <= max_row:
            point_grid[current_row][column].filled = True
            current_row += 1

    # horizontal line
    else:

        # line start and stop x vals
        if point1.x < point2.x:
            min_column = point1.x
            max_column = point2.x
        else:
            min_column = point2.x
            max_column = point1.x

        row = point1.y
        current_column = min_column

        # fill each Point in the line
        while current_column <= max_column:
            point_grid[row][current_column].filled = True
            current_column += 1



# simulates a single unit of sand falling through the provided grid
# returns False if the sand lands on its source (500,0)
# returns True otherwise
def FillSand(point_grid):

    # sand always starts from (500,0)
    current_x = 500
    current_y = 0

    # move sand downward until no longer able to do so
    # at current_y = max_fall_distance - 1, sand will be on the floor
    max_fall_distance = len(point_grid) - 1
    while current_y < max_fall_distance:
    
        # if space below is empty, move sand down 1
        if not point_grid[current_y + 1][current_x].filled:
            current_y += 1

        # if space below is occupied, but space below and to the left is empty,
        # move sand down 1 and left 1
        elif not point_grid[current_y + 1][current_x - 1].filled:
            current_x -= 1
            current_y += 1

        # if space below and to the left is occupied, but space below and to the 
        # right is empty, move sand down 1 and right 1
        elif not point_grid[current_y + 1][current_x + 1].filled:
            current_x += 1
            current_y += 1

        # if all spaces below (directly or diagonally) are occupied, 
        # fill current space and end simulation for this unit of sand
        else:
            point_grid[current_y][current_x].filled = True

            # If current point is source, source is blocked. Return False.
            if (current_y == 0):
                return False

            # otherwise, return True
            else:
                return True



################################################################################

# create a 1000 x 166 grid of unfilled Point objects
# x vals for rock structures range from 451-509, and y vals range from 14-163
# floor is at y = 165 (2 below 163)
# grid extended horizontally from Part 1 to accomodate sand piling on floor
map = []

row = 0
while row < 166:

    new_row = []

    column = 0
    while column < 1000:
        new_point = Point(column, row)
        new_row.append(new_point)
        column += 1

    map.append(new_row)
    row += 1



# fill the points in the last row of the grid (the floor)
for point in map[-1]:
    point.filled = True

# use the input data to fill the other Points where there's rock
input_file = open("../Input/D14.txt")

for line in input_file:

    # create a list of points described by the input line
    line.strip()
    string_points = line.split(" -> ")
    points = []

    for p in string_points:
    
        point_coords = p.split(",")
        x = int(point_coords[0])
        y = int(point_coords[1])

        points.append(Point(x, y))
    
    # for each point in the list, AND for each point between those points,
    # change the point's fill status to True
    num_rock_lines = len(points) - 1
    i = 0

    while i < num_rock_lines:

        current_point = points[i]
        next_point = points[i+1]
        FillRockLine(map, current_point, next_point)

        i += 1

input_file.close()



# simulate falling sand
# count the number of sand units that come to rest before the source is blocked
sand_units = 0
while FillSand(map):
    sand_units += 1

# add in the last sand unit (the one that blocked the source)
sand_units += 1

# display results
print(sand_units)