# Solve Day 7, Puzzle 1
# https://adventofcode.com/2022/day/7

# D7P1_input.txt provides terminal output for a series of commands entered while
# navigating the communication device we were given.  

# GOAL: Find all the directories with size <= 100000, and add their sizes.
# (Files may be counted more than once.)

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

    # return the total size of all files in the directory and its subdirectories
    def GetSize(self):
        size = 0
        for item in self.contents:
            if type(item) == Directory:
                size += item.GetSize()
            elif type(item) == File:
                size += item.size
        return size

    # return a list of directories and subdirectories with size <= 100000
    def FindSmallSubDirs(self):

        # master list
        small_dirs = []

        # check the current directory
        if self.GetSize() <= 100000:
            small_dirs.append(self)

        # check each subdirectory
        for item in self.contents:
            if type(item) == Directory:

                # add small directories in the subdirectory to the master list
                small_subdirs = item.FindSmallSubDirs()
                for subdir in small_subdirs:
                    small_dirs.append(subdir)

        return small_dirs

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



# find directories with size <= 100000
small_dirs = file_tree.FindSmallSubDirs()

# tally small directory sizes and display total
total_size = 0
for dir in small_dirs:

    size = dir.GetSize()
    print("dir", dir.name, size)
    total_size += size

print("\nTotal Size:", total_size)

