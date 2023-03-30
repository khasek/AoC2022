# Solve Day 15, Puzzle 1
# https://adventofcode.com/2022/day/15

# D15P1_input.txt provides a list of locations for sensors and beacons. Sensors
# only register the nearest beacon, and distance is measured with taxicab
# geometry (Manhatten distance).

# GOAL: In the row where y=2000000, how many positions cannot contain a beacon?

# Note: My first answer (4582666) was too low. Adding one (4582667) gave me the
# correct answer. My best guess as to why is that I maybe didn't have to remove
# the position with the known beacon?

################################################################################

import re

# object holds sensor coordinates and distance to nearest beacon
class Sensor:

    def __init__(self, x_int, y_int, signal_int):
        self.x = x_int
        self.y = y_int
        self.signal_strength = signal_int

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



# calculate the number of places in row 2000000 where there COULDN'T be a beacon
target_row = 2000000

# create and store a range of x values covered by each beacon
# ranges will be stored as an ordered pair [range_start, range_end]
print("Creating coverage ranges...")
coverage_ranges = []
for sensor in sensors:

    # check whether the target row is in range of the current sensor
    distance_to_row = abs(sensor.y - target_row)
    if distance_to_row <= sensor.signal_strength:

        # remaining signal strength at point on target row closest to sensor
        distance_from_center = sensor.signal_strength - distance_to_row

        # find the leftmost x value covered by the sensor signal
        current_x = sensor.x
        distance_left = 0
        while distance_left < distance_from_center:
            current_x -= 1
            distance_left += 1

        min_x = current_x

        # find the rightmost x value covered by the sensor signal
        current_x = sensor.x
        distance_right = 0
        while distance_right < distance_from_center:
            current_x += 1
            distance_right += 1

        max_x = current_x

        # add coverage range to the list
        coverage_ranges.append([min_x, max_x])



# account for overlap between sensor ranges
print("Removing overlap...")

# Python sorts lists of lists by each element in turn (compares 0, then 1, ...)
# sorting here makes it easier to address range overlap
coverage_ranges.sort()

# create a new list of ranges
# ranges here will be expanded if they overlap a range in the original list
# a new range will be added only if there's no overlap
separated_ranges = [coverage_ranges[0]]

# check for overlap between ranges in the first list and ranges in the second
for range in coverage_ranges:

    cov_range_start = range[0]
    cov_range_end = range[1]

    # because both lists are sorted, only the last item in the separated list
    # needs to be checked
    sep_range_start = separated_ranges[-1][0]
    sep_range_end = separated_ranges[-1][1]

    # if no overlap, append range to separated list
    if (cov_range_start > sep_range_end):
        separated_ranges.append(range)

    # if partial overlap, extend range in separated list
    elif (cov_range_end > sep_range_end):
        separated_ranges[-1][1] = cov_range_end

    # if complete overlap, nothing needs to be done



# calculate the number of covered positions at y = 2000000
print("Calculating covered positions...")
total_positions_covered = 0
for range in separated_ranges:
    total_positions_covered += (range[1] - range[0])


# Note: I believe this step was unnecessary; there was one beacon in the target
# row, and my original answer was short by exactly one. I'm leaving this here 
# in case it's relevant for Part 2.

# print("\nSeparated ranges:", separated_ranges)
# print("Beacon in target row:", beacons[-1])

# # discount any locations where a beacon is already known to be present
# total_beacons_in_row = 0
# for beacon in beacons:
#     if beacon[1] == target_row:
#         total_beacons_in_row += 1

# total_positions_covered -= total_beacons_in_row

# display results
print("\nResult:", total_positions_covered)