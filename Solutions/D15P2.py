# Solve Day 15, Puzzle 2
# https://adventofcode.com/2022/day/15

# D15P1_input.txt provides a list of locations for sensors and beacons. Sensors
# only register the nearest beacon, and distance is measured with taxicab
# geometry (Manhatten distance). FOR PART 2, it has been determined that a 
# distress signal is coming from a beacon with x and y values each between 0 and
# 4000000 (inclusive). Furthermore, tuning frequencies can now be calculated
# (multiply x by 4000000, then add y).

# GOAL: There should only be one possible position for the distress signal to be
# coming from. What is the tuning frequency for that location?

################################################################################

import re

# object holds sensor coordinates and distance to nearest beacon
class Sensor:

    def __init__(self, x_int, y_int, signal_int):
        self.x = x_int
        self.y = y_int
        self.signal_strength = signal_int
        self.min_x = self.x - self.signal_strength
        self.max_x = self.x + self.signal_strength
        self.min_y = self.y - self.signal_strength
        self.max_y = self.y + self.signal_strength

    def __eq__(self, other):
        if self.signal_strength == other.signal_strength:
            return True
        return False

    def __lt__(self, other):
        if self.signal_strength < other.signal_strength:
            return True
        return False

    def __gt__(self, other):
        if self.signal_strength > other.signal_strength:
            return True
        return False

    # Check all points along a sensor's perimeter (skip sections where either x
    # or y isn't between 0 and 4000000). Return the target point [x,y] if 
    # located. Otherwise, return [-1,-1].
    def CheckPerimeter(self):

        # skip this sensor if obviously out of the 0-4000000 range
        # (these aren't the only cases, just the easiest to check for)
        if (
            (self.max_x < 0) or
            (self.min_x > 4000000) or
            (self.max_y < 0) or
            (self.min_y > 4000000)
        ):
            return [-1,-1]

        # start at the top and travel clockwise
        # skip sections where x or y is <0 or >4000000
        y_current = self.min_y - 1
        x_current = self.x

        # Quadrant 1: move down and to the right
        while (y_current < self.y) and (x_current >= self.x):

            # if y is too big, skip to start of Quadrant 4
            if (y_current > 4000000):
                y_current = self.y
                x_current = self.min_x - 1

            # if x is too big, skip to start of Quadrant 2
            elif (x_current > 4000000):
                y_current = self.y
                x_current = self.max_x + 1

            # if y is too small, move y to 0 and adjust x
            elif (y_current < 0):
                y_diff = abs(self.y)
                y_current = 0
                x_current = self.max_x + 1 - y_diff

            # if x is too small, move x to 0 and adjust y
            elif (x_current < 0):
                x_diff = abs(self.x)
                y_current = self.min_y - 1 + x_diff
                x_current = 0

            # if in 0-4000000 range, check for target point
            elif NearbySensors(x_current, y_current, sensors) == 0:
                return [x_current, y_current]
            
            # if in 0-4000000 range but not target point, move diagonally
            else:
                y_current += 1
                x_current += 1

        # Quadrant 2: move down and to the left
        while (y_current >= self.y) and (x_current > self.x):

            # if x is too small, end perimeter check
            if (x_current < 0):
                return [-1,-1]

            # if y is too big, skip to start of Quadrant 3
            elif (y_current > 4000000):
                y_current = self.max_y + 1
                x_current = self.x

            # if y is too small, move y to 0 and adjust x
            elif (y_current < 0):
                y_diff = abs(self.y)
                y_current = 0
                x_current = self.max_x + 1 - y_diff

            # if x is too big, move x to 4000000 and adjust y
            elif (x_current > 4000000):
                x_diff = abs(4000000 - self.x)
                y_current = self.max_y + 1 - x_diff
                x_current = 4000000

            # if in 0-4000000 range, check for target point
            elif NearbySensors(x_current, y_current, sensors) == 0:
                return [x_current, y_current]
            
            # if in 0-4000000 range but not target point, move diagonally
            else:
                y_current += 1
                x_current -= 1

        # Quadrant 3: move up and to the left
        while (y_current > self.y) and (x_current <= self.x):

            # if y is too small, end perimeter check
            if (y_current < 0):
                return [-1,-1]

            # if x is too small, skip to start of Quadrant 4
            if (x_current < 0):
                y_current = self.y
                x_current = self.min_x - 1

            # if y is too big, move y to 4000000 and adjust x
            if (y_current > 4000000):
                y_diff = abs(4000000 - self.y)
                y_current = 4000000
                x_current = self.min_x - 1 + y_diff

            # if x is too big, move x to 4000000 and adjust y
            elif (x_current > 4000000):
                x_diff = abs(4000000 - self.x)
                y_current = self.max_y + 1 - x_diff
                x_current = 4000000

            # if in 0-4000000 range, check for target point
            elif NearbySensors(x_current, y_current, sensors) == 0:
                return [x_current, y_current]
            
            # if in 0-4000000 range but not target point, move diagonally
            else:
                y_current -= 1
                x_current -= 1

        # Quadrant 4: move up and to the right
        while (y_current <= self.y) and (x_current < self.x):

            # if y is too small or x is too big, end perimeter check
            if (y_current < 0) or (x_current > 4000000):
                return [-1,-1]

            # if y is too big, move y to 4000000 and adjust x
            if (y_current > 4000000):
                y_diff = abs(4000000 - self.y)
                y_current = 4000000
                x_current = self.min_x - 1 + y_diff

            # if x is too small, move x to 0 and adjust y
            elif (x_current < 0):
                x_diff = abs(self.x)
                y_current = self.min_y - 1 + x_diff
                x_current = 0

            # if in 0-4000000 range, check for target point
            elif NearbySensors(x_current, y_current, sensors) == 0:
                return [x_current, y_current]
            
            # if in 0-4000000 range but not target point, move diagonally
            else:
                y_current -= 1
                x_current += 1

        # if target point not found, return [-1,-1]
        return [-1,-1]



# test whether a coordinate point is in range of a sensor
# returns True if in range, False if not
def WithinRange(x_coordinate, y_coordinate, sensor):

    x_diff = abs(x_coordinate - sensor.x)
    y_diff = abs(y_coordinate - sensor.y)

    if sensor.signal_strength >= (x_diff + y_diff):
        return True
    
    return False

# returns the number of sensors in range of a given point
def NearbySensors(x_coordinate, y_coordinate, list_of_sensors):

    num_sensors = 0
    for sensor in list_of_sensors:

        if WithinRange(x_coordinate, y_coordinate, sensor):
            num_sensors += 1

    return num_sensors

################################################################################

# parse puzzle input to create a list of sensors
sensors = []

# also need to keep track of beacon coordinates [x, y]
beacons = []

print("Parsing file...")
input_file = open("../Input/D15.txt")

for line in input_file:

    # EXAMPLE LINE:
    # Sensor at x=278431, y=3878878: closest beacon is at x=-1050422, y=3218536

    # pull out coordinates for sensor and beacon
    # sensor will always be listed before beacon
    x_coords = re.findall("x=[\-0-9]*", line)
    y_coords = re.findall("y=[\-0-9]*", line)

    # sensor coordinates
    SX = int(x_coords[0].split("=")[1])
    SY = int(y_coords[0].split("=")[1])

    # beacon coordinates
    BX = int(x_coords[1].split("=")[1])
    BY = int(y_coords[1].split("=")[1])

    # calculate the distance between the sensor and the beacon
    x_diff = abs(SX - BX)
    y_diff = abs(SY - BY)

    total_distance = x_diff + y_diff

    # instantiate a new sensor and add it to the list
    new_sensor = Sensor(SX, SY, total_distance)
    sensors.append(new_sensor)

    # mark the beacon location, if it hasn't already been marked
    # some sensors register the same beacon
    if [BX, BY] not in beacons:
        beacons.append([BX, BY])

input_file.close()



# sort sensors by signal strength to make the next step faster (shortest first)
sensors.sort()

# the target point will lie next to the perimeter of at least one sensor's range
# check each sensor's perimeter until the target point is found
for sensor in sensors:

    print("Checking sensor perimeter...")
    perim_check_results = sensor.CheckPerimeter()

    if perim_check_results != [-1,-1]:
        print("POINT FOUND:", perim_check_results)
        tuning_frequency = (4000000 * perim_check_results[0]) + perim_check_results[1]
        print("\nTuning frequency:", tuning_frequency)
        break

    else:
        print("No point found\n")