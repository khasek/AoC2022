# Solve Day 16, Puzzle 1
# https://adventofcode.com/2022/day/16

# D16P1_input.txt provides an analysis of an interconnected system of pressure
# release valves. Each valve releases a given amount of pressure per minute when
# open. It takes one minute to open a valve (valves all start out closed), and
# it takes one minute to travel from one valve to another. We have 30 minutes to
# release as much pressure as possible, before the volcano erupts around us!

# GOAL: What is the maximum amount of pressure that can be released in the 30
# minutes we have available?

################################################################################

import re



# Valve graph should be a dictionary with keys as valve names and vals
# as the valves themselves. Valves should be objects with 3 attributes:
# name (string), flow rate (int) and connections. Connections are another 
# dictionary, with connecting valve names for keys and path weights for vals.



# this class will only be used for valve AA (the starting point) and valves with
# flow rate > 0 (there are 15 such valves in my puzzle input)
class Valve:

    def __init__(self, name:str, fr:int):
        self.name = name
        self.flow_rate = fr
        self.connections = {}

    # c_name: name of the connected valve (ex: "AA")
    # distance: number of minutes it takes to reach that valve and open it
    def AddConnection(self, c_name:str, distance:int):
        self.connections[c_name] = distance



# Recursively finds the shortest path between two valves
def ShortestPath(tunnel_graph:dict, start:str, end:str, visited:list) -> int:

    visited.append(start)

    # there are 54 valves in my puzzle input
    min_path = 54

    # testing...
    print(visited)

    # compare the shortest paths to the target from each valve that connects
    # to the current one
    for connection in tunnel_graph[start]:

        # testing...
        print(connection)

        # no need to keep going if one of those connections is the target
        if (connection == end):
            return 2

        # also skip any connections that have already been visited
        elif (connection not in visited):

            # recursively find the shortest path from this connected valve
            path = ShortestPath(tunnel_graph, connection, end, visited)

            # note if shorter than paths from other connections
            if (path < min_path):
                min_path = path

    return min_path



# Recursively calculates the max pressure released from a set of valves
def CalculateMaxPressure(valve_graph:dict, current_valve:str, 
                         unopened_valves:list, minutes_remaining:int) -> int:

    unopened_valves.remove(current_valve)
    current_pressure = minutes_remaining * valve_graph[current_valve].flow_rate
    max_remaining = 0

    for valve in unopened_valves:

        # update time remaining once new valve is open
        updated_minutes = minutes_remaining - valve_graph[current_valve].connections[valve]

        # if there isn't enough time to reach this valve, remove it from consideration
        if (updated_minutes <= 0):
            unopened_valves.remove(valve)

        # if there is enough time, recursively check the max pressure that can
        # be released by going to this valve next
        else:
            pressure = CalculateMaxPressure(valve_graph, valve, unopened_valves, updated_minutes)

            # note the pressure released by this valve if it's greather than
            # the pressure released by other valves
            if (pressure > max_remaining):
                max_remaining = pressure

    # Add the pressure released by the current valve to the maximum amount of
    # pressure that can be released by remaining valves. Return that total.
    total_pressure = current_pressure + max_remaining
    return total_pressure
        

    
################################################################################

# will be used to find the path with the greatest pressure release
# key: valve name
# value: Valve object with flow rate > 0 (or the starting valve)
useful_valves = {}

# will be used to find shortest paths between valves with flow rate > 0
# key: valve name
# value: list of connecting valve names (flow rate unimportant)
tunnel_map = {}

# parse puzzle input for valve data
input_file = open("../Input/D16.txt")

for line in input_file:

    # Sample line:
    # "Valve ZZ has flow rate=10; tunnels lead to valves II, GR, HA, BO, TN"

    # valve name
    name_section = re.findall("Valve [A-Z]{2}", line)
    name_string = name_section[0].split()[1]

    # valve flow rate
    flow_section = re.findall("flow rate=[0-9]+", line)
    flow_int = int(flow_section[0].split("=")[1])

    # connected valves
    connections_section = re.findall("valve[s]? [A-Z,\s]+", line)
    connections_string = re.sub("valve[s]? ", "", connections_section[0])
    connections_list = connections_string.strip().split(", ")

    # update valve graphs
    tunnel_map[name_string] = connections_list

    if (flow_int > 0) or (name_string == "AA"):
        useful_valves[name_string] = Valve(name_string, flow_int)

input_file.close()



# # testing...

# counter = 1
# for valve in useful_valves:

#     print(counter, ":", valve, useful_valves[valve])
#     counter += 1

# print()
# counter = 1
# for valve in tunnel_map:

#     print(counter, ":", valve, tunnel_map[valve])
#     counter += 1

# # ...caught a parsing error, now we're good!



# more testing...
print(ShortestPath(tunnel_map, "ZZ", "ZQ", []))



# # fill in connection distances between valves with flow rate > 0
# for valve in useful_valves:

#     # testing...
#     print("Finding connections for Valve", valve)

#     for other_valve in useful_valves:

#         # connect every valve to every other valve
#         if ((valve != other_valve) and 
#             (useful_valves[valve].connections.get(other_valve)) is None):

#             distance = ShortestPath(tunnel_map, valve, other_valve, [])

#             # testing...
#             print(valve, "->", other_valve, distance)

#             useful_valves[valve].AddConnection(other_valve, distance)
#             useful_valves[other_valve].AddConnection(valve, distance)

# # # ...errors resolved, carry on!



# # use this list to track which valves have yet to be opened
# unopened_valves = []
# for valve in useful_valves:
#     unopened_valves.append(valve)

# # calculate the maximum pressure that can be released in 30 minutes
# max_pressure_released = CalculateMaxPressure(useful_valves, "AA", unopened_valves, 30)

# # display results
# print(max_pressure_released)


