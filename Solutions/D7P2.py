# Solve Day 7, Puzzle 2
# https://adventofcode.com/2022/day/7

# D7P1_input.txt provides terminal output for a series of commands entered while
# navigating the communication device we were given. The device has a diskspace
# of 70,000,000. You need 30,000,000 free in order to run an update.

# GOAL: Find all the directories that are large enough to free up sufficient 
# disk space for the update if they were deleted. Submit the size of the 
# smallest such directory.

# Notes: I had trouble with my first attempt at solving this problem, so I
# decided to change tactics and make this new file. SO GLAD I GOT THIS FINALLY, 
# IT TOOK ME THREE DAYS.

################################################################################

import re



# File class contains a name and a size
# name should be a string, and size should be a positive integer
class File:

    def __init__(self, file_name, file_size):
        self.name = file_name
        self.size = file_size



# Directory class contains name, parent, and a list of files and subdirectories
class Directory:

    def __init__(self, dir_name):
        self.name = dir_name
        self.parent = None
        self.contents = []

    def __eq__(self, other):
        if self.GetSize() == other.GetSize():
            return True
        else:
            return False

    def __gt__(self, other):
        if self.GetSize() > other.GetSize():
            return True
        else:
            return False

    def __ge__(self, other):
        if self.GetSize() >= other.GetSize():
            return True
        else:
            return False

    def __lt__(self, other):
        if self.GetSize() < other.GetSize():
            return True
        else:
            return False

    def __le__(self, other):
        if self.GetSize() <= other.GetSize():
            return True
        else:
            return False

    # return the total size of all files in the directory and its subdirectories
    def GetSize(self):
        size = 0
        for item in self.contents:
            if type(item) == Directory:
                size += item.GetSize()
            elif type(item) == File:
                size += item.size
        return size

    # return a list of directories and subdirectories with the specified size
    # accepts <, <=, >, >=, or = for the comparison operator
    def GetDirsBySize(self, target_size, comparison_operator):

        # master list
        target_dirs = []

        # check the current directory's size
        if (comparison_operator == "<") and (self.GetSize() < target_size):
            target_dirs.append(self)
        elif (comparison_operator == "<=") and (self.GetSize() <= target_size):
            target_dirs.append(self)
        elif (comparison_operator == ">") and (self.GetSize() > target_size):
            target_dirs.append(self)
        elif (comparison_operator == ">=") and (self.GetSize() >= target_size):
            target_dirs.append(self)
        elif (comparison_operator == "=") and (self.GetSize() == target_size):
            target_dirs.append(self)

        # check each subdirectory
        for item in self.contents:
            if type(item) == Directory:

                # add appropriately-sized directories in the subdirectory to the master list
                target_subdirs = item.GetDirsBySize(target_size, comparison_operator)
                for subdir in target_subdirs:
                    target_dirs.append(subdir)

        return target_dirs

    # for testing
    def DisplayDirectory(self, file):

        f = open(file, "a")

        dir_size = self.GetSize()

        output_string = "\nDirectory: " + self.name + " " + str(dir_size)
        f.write(output_string)
        f.close()

        for item in self.contents:

            if type(item) == Directory:
                item.DisplayDirectory(file)

            # elif type(item) == File:
            #     print("File:", item.name, item.size)

################################################################################

input_file = open("../Input/D7.txt")

# create root directory for file tree
file_tree = Directory("/")

# use this variable to navigate up and down the file tree
dir_current = file_tree

# navigate and fill file tree
# assumes directories are not accessed with cd before being listed with ls
# CHECK WHETHER THIS IMPLEMENTATION CHANGES THE INPUT FILE
for line in input_file:

    # testing...
    # print("Current directory:", dir_current)

    # line reads "$ cd directory_name"
    if re.search("\$ cd [a-z]", line):

        # find the name of the directory that is being called
        new_dir_name = re.sub("\$ cd ", "", line).strip()

        # testing...
        # print("Calling directory", new_dir_name)
        
        # search the current directory's contents for a directory of that name
        # update the current directory
        for item in dir_current.contents:
            if (type(item) == Directory) and (item.name == new_dir_name):

                # testing...
                # print("Found child directory", new_dir_name)

                dir_current = item
                break

    # line reads "$ cd .."
    elif re.search("\$ cd \.\.", line):

        # navigate to parent directory
        dir_current = dir_current.parent

        # testing...
        # print("..")

    # line reads "file_size file_name"
    elif re.search("[0-9]+ [a-z]", line):

        # parse line for file data
        file_parts = line.split()
        file_size = int(file_parts[0])
        file_name = file_parts[1].strip()

        # testing...
        # print("Making file", file_name)

        # check whether this file has already been made
        # e.g. if the contents of dir_current are listed more than once
        dir_content_names = []
        for item in dir_current.contents:
            if type(item) == File:
                dir_content_names.append(item.name)
        
        if file_name not in dir_content_names:

            # create file and add to current directory's contents
            new_file = File(file_name, file_size)
            dir_current.contents.append(new_file)

    # line reads "dir dir_name"
    elif re.search("dir [a-z]", line):

        # parse line for subdirectory name
        line_parts = line.split()
        subdir_name = line_parts[1].strip()

        # testing...
        # print("Making directory", subdir_name)

        # check whether this directory has already been made
        # e.g. if the contents of dir_current are listed more than once
        dir_content_names = []
        for item in dir_current.contents:
            if type(item) == Directory:
                dir_content_names.append(item.name)

        if subdir_name not in dir_content_names:

            # create new directory and add to current directory's contents
            new_subdir = Directory(subdir_name)
            new_subdir.parent = dir_current
            dir_current.contents.append(new_subdir)

    # if line reads "$ cd /"
    elif re.search("\$ cd /", line):

        # navigate to root directory
        dir_current = file_tree

        # testing...
        # print("Going to root directory")

    # if line reads "$ ls", simply continue to the next line

input_file.close()

# for testing
#file_tree.DisplayDirectory("D7_test.txt")



# current disk space usage
current_space_used = file_tree.GetSize()

# free space available
current_free_space = 70000000 - current_space_used

# directories need to be at least this large in order to free up enough space
space_needed = 30000000 - current_free_space

# directories that are large enough to free up sufficient space
large_dirs = file_tree.GetDirsBySize(space_needed, ">=")

# sort by ascending order, so the smallest directory will be listed first
large_dirs.sort()

# display smallest directory of appropriate size
print(large_dirs[0].name, large_dirs[0].GetSize())
