# Solve Day 8, Puzzle 2
# https://adventofcode.com/2022/day/8

# D8P1_input.txt provides a grid of single-digit numbers representing trees of
# varying heights (0 for the shortest, 9 for the tallest). A tree's scenic score
# is calculated by multiplying how many trees are visible from each direction. 
# To find visibility in any particular direction, count trees in that direction 
# and "stop if you reach an edge or at the first tree that is the same height or 
# taller than the tree under consideration."

# GOAL: Find the most scenic tree in the grove, and submit its score.

# Notes: First answer of 300,000 was too high. I manually checked the score for
# my top-scoring tree, and it should have been 268,912 (49 * 49 * 8 * 14). 
# Conveniently, 50 * 50 * 8 * 15 = 300,000. Must be an off-by-one error.
# UPDATE: That was it!

################################################################################

# comparison operators are overloaded to enable sorting
class Tree:

    def __init__(self, row, column, height, scenic_score):
        self.row = row
        self.column = column
        self.height = height
        self.score = scenic_score
    
    def __eq__(self, other):
        if self.score == other.score:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.score > other.score:
            return True
        else:
            return False

    def __ge__(self, other):
        if self.score >= other.score:
            return True
        else:
            return False

    def __lt__(self, other):
        if self.score < other.score:
            return True
        else:
            return False

    def __le__(self, other):
        if self.score <= other.score:
            return True
        else:
            return False

################################################################################

input_file = open("../Input/D8.txt")

# store data as a list of lists of integers
tree_rows = []
for line in input_file:

    # remove the newline character
    just_numbers = line.strip()

    # construct the row
    row = []
    for char in just_numbers:
        row.append(int(char))

    tree_rows.append(row)

input_file.close()


# create a list of Trees
# this will be sorted later to find the tree with the highest scenic score
grove = []

grove_width = len(tree_rows[0]) # all rows have the same length
grove_height = len(tree_rows)

# all trees on the outside of the grid have a score of 0, so they can be ignored
# iterate through rows, excluding the first and last
row = 1
while row < (grove_height - 1):

    current_row = tree_rows[row]

    # iterate through columns, excluding the first and last
    column = 1
    while column < (grove_width - 1):

        current_tree_height = current_row[column]

        # calculate visibility to the west/left
        western_score = 1

        column_iter = column - 1
        while (column_iter > 0) and (current_tree_height > tree_rows[row][column_iter]):
            western_score += 1
            column_iter -= 1

        # calculate visibility to the east/right
        eastern_score = 1

        column_iter = column + 1
        while (column_iter < grove_width - 1) and (current_tree_height > tree_rows[row][column_iter]):
            eastern_score += 1
            column_iter += 1

        # calculate visibility to the north/top
        northern_score = 1

        row_iter = row - 1
        while (row_iter > 0) and (current_tree_height > tree_rows[row_iter][column]):
            northern_score += 1
            row_iter -= 1

        # calculate visibility to the south/bottom
        southern_score = 1

        row_iter = row + 1
        while (row_iter < grove_height - 1) and (current_tree_height > tree_rows[row_iter][column]):
            southern_score += 1
            row_iter += 1

        # calculate total scenic score
        scenic_score = northern_score * southern_score * eastern_score * western_score

        # add Tree object to list
        new_tree = Tree(row, column, current_tree_height, scenic_score)
        grove.append(new_tree)

        column += 1

    row += 1



# sort the list of trees so the tree with the best score will be listed first
grove.sort(reverse=True)

# display results
print("Top 10 Trees:")

i = 0
while i < 10:

    row = str(grove[i].row)
    column = str(grove[i].column)
    height = str(grove[i].height)
    score = str(grove[i].score)

    message = row + "-" + column + " " + height + " " + score
    print(message)

    i += 1

print("\nHighest Scenic Score:", grove[0].score)
