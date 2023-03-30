# Solve Day 12, Puzzle 2
# https://adventofcode.com/2022/day/12

# D12P1_input.txt provides a grid of lowercase letters a-z. The grid represents
# a topographical map that you can move through one space at a time (up, down, 
# left, or right). Individual letters represent elevation, with "a" being the 
# lowest and "z" being the highest; you can only move directly to the next 
# letter in the alphabet (a to b, but not a to c).

# GOAL: Find the shortest path from ANY coordinate at elevation "a" to the 
# target position "E". Submit the number of steps it took.

################################################################################

class Coordinate:

    # elevation is the character a-z at a spot on the map
    def __init__(self, row, column, elevation, previous_coord):
        self.x = column
        self.y = row
        self.z = elevation
        self.parent = previous_coord
        self.children = []

    def __eq__(self, other):
        if (self.x == other.x and self.y == other.y and self.z == other.z):
            return True
        else:
            return False

    # return True if able to move from this Coordinate to another
    def Path(self, other):
        
        x_diff = abs(self.x - other.x)
        y_diff = abs(self.y - other.y)
        z_diff = ord(other.z) - ord(self.z)

        # ADDENDUM FOR PART 2: Disalow movement to a coordinate at elevation "a" 
        # (if a path moves to "a" at any point, the path starting from that 
        # second "a" will be shorter)

        if  (other.z != "a") and (z_diff <= 1) and (
            (x_diff == 0 and y_diff == 1) or 
            (x_diff == 1 and y_diff == 0)
        ):
            return True

        else:
            return False

    # returns True if other is a descendant of self (or equal to self)
    def Descendant(self, other):

        # check current node first
        if self == other:
            return True
        elif self.children == []:
            return False
        
        # recursively check current node's children
        for child in self.children:
            if child.Descendant(other):
                return True
        
        # return False if no matches found
        return False

    # return a descendant Coordinate with the given x/y/z values
    def GetDescendant(self, target_x, target_y, target_z):

        target = Coordinate(target_y, target_x, target_z, None)

        for child in self.children:
            if child == target:
                return child
            elif child.Descendant(target):
                return child.GetDescendant(target_x, target_y, target_z)

    # add child coordinates for the current coordinate
    def AddChildren(self, root):

            x = self.x
            y = self.y

            # add coordinate to the left
            if x > 0:
                left_coord = Coordinate(y, x-1, map[y][x-1], self)
                if (not root.Descendant(left_coord)) and self.Path(left_coord):
                    self.children.append(left_coord)

            # add coordinate to the right
            if x < len(map[0]) - 1:
                right_coord = Coordinate(y, x+1, map[y][x+1], self)
                if (not root.Descendant(right_coord)) and self.Path(right_coord):
                    self.children.append(right_coord)

            # add coordinate above
            if y > 0:
                up_coord = Coordinate(y-1, x, map[y-1][x], self)
                if (not root.Descendant(up_coord)) and self.Path(up_coord):
                    self.children.append(up_coord)

            # add coordinate below
            if y < len(map) - 1:
                down_coord = Coordinate(y+1, x, map[y+1][x], self)
                if (not root.Descendant(down_coord)) and self.Path(down_coord):
                    self.children.append(down_coord)

    # return depth of coordinate node in a graph with the provided root node
    # returns -1 if the current node is not a descendant of the provided root
    def GetDepth(self, root):

        if root.Descendant(self):
            depth = 0
            current = self
            while current != root:
                depth += 1
                current = current.parent

            return depth
        else:
            return -1
    
    # return a list of all coordinate nodes at the same depth in a tree graph
    def GetSiblings(self, root):

        if self == root:
            return [root]

        else:
            target_depth = self.GetDepth(root)

            coords_in_level = root.children
            graph_level = 1

            while graph_level < target_depth:

                new_coords = []
                for coord in coords_in_level:
                    new_coords.extend(coord.children)

                coords_in_level = new_coords
                graph_level += 1

            return coords_in_level
    
    # create a tree graph with the current coordinate as the root
    # fills the graph breadth-first to find the shortest path to any node
    def CreatePaths(self, tree_root):

        # add the next level of coordinate nodes
        # GetSiblings() returns a list that includes the current node
        siblings = self.GetSiblings(tree_root)
        for sibling in siblings:
            sibling.AddChildren(tree_root)

        # if any nodes were added to the next level, repeat
        for sibling in siblings:
            if sibling.children != []:
                sibling.children[0].CreatePaths(tree_root)
                break  

################################################################################

# build the map
input_file = open("../Input/D12.txt")

map = []
for line in input_file:
    row = line.strip()
    map.append(row)

input_file.close()

# assign elevation values to start and stop coordinates (both on line 21)
map[20] = map[20].replace("S", "a")
map[20] = map[20].replace("E", "z")

# check the shortest path to target from each location on the map with elevation 
# "a"; store the number of steps it took in this list for later comparison
paths = []

# first find all the spots with elevation "a"
number_of_rows = len(map)
number_of_columns = len(map[0])

row = 0
while row < number_of_rows:

    column = 0
    while column < number_of_columns:

        if map[row][column] == "a":

            # display a message so I know everything is running properly
            # (creating trees sometimes takes a few seconds)
            progress_message = "Checking path from (" + str(column) + "," + str(row) + ")"
            print(progress_message)

            # create a tree graph with the current position as the root
            new_start = Coordinate(row, column, "a", None)
            new_start.CreatePaths(new_start)

            # if the graph reached our target coordinate, 
            # store the number of steps it took
            path_end = new_start.GetDescendant(58, 20, "z")
            if type(path_end) == Coordinate:
                path_length = int(path_end.GetDepth(new_start))
                print("\nPATH FOUND:", path_length)

                paths.append(path_length)
                print(paths, "\n")

        column += 1

    row += 1

# sort the list of paths in ascending order (shortest path listed first)
paths.sort()

# display results
print("")
print(paths)
print("\nSteps in the shortest possible path:", paths[0])
