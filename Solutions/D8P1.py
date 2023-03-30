# Solve Day 8, Puzzle 1
# https://adventofcode.com/2022/day/8

# D8P1_input.txt provides a grid of single-digit numbers representing trees of
# varying heights (0 for the shortest, 9 for the tallest). Trees are visible if
# they are taller than all the other trees in some direction.

# GOAL: Find how many trees are visible from outside the grove.

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

# testing...
# for row in tree_rows:
#     print(row)



# all trees on the outside of the grid are visible
grove_width = len(tree_rows[0])
grove_height = len(tree_rows)
grove_perimeter = (2 * grove_width) + (2 * grove_height) - 4

# total visible trees so far
visible_trees = grove_perimeter

# add how many trees on the inside of the grid are visible

# iterate through rows, excluding the first and last
row = 1
while row < (grove_height - 1):

    current_row = tree_rows[row]

    # iterate through columns, excluding the first and last
    column = 1
    while column < (grove_width - 1):

        current_tree_height = current_row[column]

        # check visibility from the left

        # find trees in the same row, but a lower column
        trees_left = []
        left_iter = 0

        while left_iter < column:
            trees_left.append(current_row[left_iter])
            left_iter += 1

        # compare heights
        visible = True

        for tree in trees_left:
            if tree >= current_tree_height:
                visible = False
                break

        # if visible from the left, increment count and move to next tree
        # if not visible from the left, check visibility from the right
        if visible:
            visible_trees += 1

        else:

            # find trees in the same row, but a higher column
            trees_right = []
            right_iter = column + 1

            while right_iter < grove_width:
                trees_right.append(current_row[right_iter])
                right_iter += 1

            # compare heights
            visible = True

            for tree in trees_right:
                if tree >= current_tree_height:
                    visible = False
                    break

            # if visible from the right, increment count and move to next tree
            # if not visible from the right, check visibility from above
            if visible:
                visible_trees += 1

            else:

                # find trees in a higher row, but the same column
                trees_above = []
                above_iter = 0

                while above_iter < row:
                    trees_above.append(tree_rows[above_iter][column])
                    above_iter += 1

                # compare heights
                visible = True

                for tree in trees_above:
                    if tree >= current_tree_height:
                        visible = False
                        break

                # if visible from above, increment count and move to next tree
                # if not visible from above, check visibility from below
                if visible:
                    visible_trees += 1

                else:

                    # find trees in a lower row, but the same column
                    trees_below = []
                    below_iter = row + 1

                    while below_iter < grove_height:
                        trees_below.append(tree_rows[below_iter][column])
                        below_iter += 1

                    # compare heights
                    visible = True

                    for tree in trees_below:
                        if tree >= current_tree_height:
                            visible = False
                            break

                    # if visible from below, increment count
                    # if not, tree is not visible -- move to next tree
                    if visible:
                        visible_trees += 1

        column += 1

    row += 1



# display results
print("Total Trees:", grove_width*grove_height)
print("Visible Trees:", visible_trees)