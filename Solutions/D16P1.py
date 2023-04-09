# Solve Day 16, Puzzle 1
# https://adventofcode.com/2022/day/16

# D16P1_input.txt provides an analysis of an interconnected system of pressure
# release valves. Each valve releases a given amount of pressure per minute when
# open. It takes one minute to open a valve (valves all start out closed), and
# it takes one minute to travel from one valve to another. We have 30 minutes to
# release as much pressure as possible, before the volcano erupts around us!

# GOAL: What is the maximum amount of pressure that can be released in the 30
# minutes we have available?

# Note: I refactored this one a couple times before arriving at my first guess,
# 712, which was too low. 

################################################################################

import re



# Valve graph should be a dictionary with keys as valve names and vals
# as the valves themselves. Valves should be objects with 3 attributes:
# name (string), flow rate (int) and connections. Connections are another 
# dictionary, with connecting valve names for keys and path weights for vals.



# will be used to to store valve connections, regardless of flowrate
class TunnelSystem:

    # member variable: system (dict)
    #   key: valve name (string)
    #   value: list of connected valve names (strings)
    def __init__(self):
        self.system = {}

    def AddValve(self, valve_name:str, valve_connections:list):
        self.system[valve_name] = valve_connections

    # find the length of the shortest path between start and end valves
    def ShortestPath(self, start:str, end:str) -> int:
        visited = []
        return self.__ShortestPath(start, end, visited)
    
    # find the length of the shortest path between start and end valves
    def __ShortestPath(self, start:str, end:str, visited:list) -> int:

        # recursive base case
        # return 1 instead of 0 to account for the time it takes to open a valve
        if (start == end):
            return 1
        
        visited.append(start)

        # there are 54 valves in my puzzle input
        min_path = 54

        for connection in self.system[start]:

            if (connection not in visited):

                distance = self.__ShortestPath(connection, end, visited) + 1

                if distance < min_path:
                    min_path = distance
        
        return min_path



# will only be used for valve AA (the starting point) and valves with
# flow rate > 0 (there are 15 such valves in my puzzle input)
class Valve:

    def __init__(self, name:str, fr:int):

        self.name = name
        self.flow_rate = fr

        # connections dict
        #   key: valve name (string)
        #   value: minutes to reach and open valve (int)
        self.connections = {}

    # c_name: name of the connected valve (ex: "AA")
    # distance: number of minutes it takes to reach that valve and open it
    def AddConnection(self, c_name:str, distance:int):
        self.connections[c_name] = distance

    def GetDistance(self, c_name:str) -> int:
        return self.connections[c_name]



# will be used to track distances between valves with flow rate > 0
class ValveNetwork:

    # member variable: graph (dict)
    #   key: valve name (string)
    #   value: valve with flow rate > 0 (Valve)
    def __init__(self):
        self.graph = {}

    def AddValve(self, name, flow_rate):
        self.graph[name] = Valve(name, flow_rate)

    # calculate the maximum amount of pressure that can be released from
    # the valve network in 30 minutes, starting at valve AA
    def CalculateMaxPressure(self) -> int:

        unopened = []

        for key in self.graph:
            unopened.append(key)

        return self.__CalculateMaxPressure("AA", unopened, 30)
    
    # recursively calculate the maximum amount of pressure that can be released
    # from a subset of valves in the time given
    def __CalculateMaxPressure(self, current:str, unopened:list, 
                               time_remaining:int) -> int:

        # recursive base case: stop when out of time or all valves visited
        if ((time_remaining <= 0) or (len(unopened) == 0)):
            return 0
        
        unopened.remove(current)
        pressure_from_current = time_remaining * self.graph[current].flow_rate
        max_additional_pressure = 0

        # find the maximum amount of pressure that can be released from 
        # remaining valves
        for valve in unopened:

            updated_time = time_remaining - self.graph[current].GetDistance(valve)
            pressure = self.__CalculateMaxPressure(valve, unopened, updated_time)

            if (pressure > max_additional_pressure):
                max_additional_pressure = pressure

        return (pressure_from_current + max_additional_pressure)
        

    
################################################################################



# will be used to find the path with the greatest pressure release
# key: valve name
# value: Valve object with flow rate > 0 (plus the starting valve AA)
valve_network = ValveNetwork()

# will be used to find shortest paths between valves with flow rate > 0
tunnel_system = TunnelSystem()

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
    tunnel_system.AddValve(name_string, connections_list)

    if (flow_int > 0) or (name_string == "AA"):
        valve_network.AddValve(name_string, flow_int)

input_file.close()



# # testing...

# counter = 1
# for valve in valve_network.graph:

#     print(counter, ":", valve, valve_network.graph[valve])
#     counter += 1

# print()
# counter = 1
# for valve in tunnel_system.system:

#     print(counter, ":", valve, tunnel_system.system[valve])
#     counter += 1

# # ...caught a parsing error, now we're good!



# # more testing...
# print(tunnel_system.ShortestPath("ZZ", "ZQ"))



# fill in connection distances between valves with flow rate > 0
for valve in valve_network.graph:

    # # testing...
    # print("Finding connections for Valve", valve)

    for other_valve in valve_network.graph:

        # connect every valve to every other valve
        if ((valve != other_valve) and 
            (valve_network.graph[valve].connections.get(other_valve)) is None):

            distance = tunnel_system.ShortestPath(valve, other_valve)

            # # testing...
            # print(valve, "->", other_valve, distance)

            valve_network.graph[valve].AddConnection(other_valve, distance)
            valve_network.graph[other_valve].AddConnection(valve, distance)

# # ...errors resolved, carry on!



# calculate the maximum pressure that can be released in 30 minutes
max_pressure_released = valve_network.CalculateMaxPressure()

# display results
print(max_pressure_released)


