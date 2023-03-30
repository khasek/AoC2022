# Solve Day 11, Puzzle 1
# https://adventofcode.com/2022/day/10

# D11P1_input.txt provides a list of monkeys who are throwing some of your 
# missing stuff around, as well as the rules by which the monkeys decide where
# to throw those items.

# GOAL: Determine which two monkeys inspect the most items after 20 rounds. 
# Submit the level of monkey business (the product of numbers of inspections).

################################################################################

import math

class Monkey:

    def __init__(self, item_list, op_symbol, op_int, test_int, 
                 throw_index_true, throw_index_false):
        self.starting_items = item_list
        self.operator = op_symbol
        self.operation_int = op_int
        self.test = test_int
        self.throw_when_true = throw_index_true
        self.throw_when_false = throw_index_false
        self.inspection_tally = 0

    def ThrowItems(self, monkey_list):
        
        for item in self.starting_items:

            # monkey inspects the item
            if self.operator == "+":
                item_after_inspection = item + self.operation_int
            elif self.operator == "*":
                item_after_inspection = item * self.operation_int
            else:
                item_after_inspection = item ** self.operation_int

            # increment the number of times this monkey has inspected an item
            self.inspection_tally += 1
            
            # relief applied for item not breaking
            finalized_item_val = math.floor(item_after_inspection / 3)

            # monkey tests worry level and throws item
            # input lists all tests as checking divisibility by provided int
            if (finalized_item_val % self.test) == 0:
                next_monkey = monkey_list[self.throw_when_true]
            else:
                next_monkey = monkey_list[self.throw_when_false]

            next_monkey.starting_items.append(finalized_item_val)

        # remove items from the monkey's list of items
        self.starting_items.clear()

################################################################################

# Because there are only 8 monkeys, it's easier to manually make them all
# (as opposed to parsing the input file)
monkey0 = Monkey([85, 79, 63, 72], "*", 17, 2, 2, 6)
monkey1 = Monkey([53, 94, 65, 81, 93, 73, 57, 92], "**", 2, 7, 0, 2)
monkey2 = Monkey([62, 63], "+", 7, 13, 7, 6)
monkey3 = Monkey([57, 92, 56], "+", 4, 5, 4, 5)
monkey4 = Monkey([67], "+", 5, 3, 1, 5)
monkey5 = Monkey([85, 56, 66, 72, 57, 99], "+", 6, 19, 1, 0)
monkey6 = Monkey([86, 65, 98, 97, 69], "*", 13, 11, 3, 7)
monkey7 = Monkey([87, 68, 92, 66, 91, 50, 68], "+", 2, 17, 4, 3)

monkeys = [monkey0, monkey1, monkey2, monkey3, monkey4, monkey5, monkey6, monkey7]



# simulate 20 rounds of monkeys throwing items
round = 0
while round < 20:

    # print("Begin round", round)

    for monkey in monkeys:
        # print("Monkey throwing items...")
        monkey.ThrowItems(monkeys)

    round += 1

# create a sorted list (descending order) for number of times each monkey inspected
inspections = []
for monkey in monkeys:
    inspections.append(monkey.inspection_tally)

inspections.sort(reverse=True)

print(inspections)
print("The level of monkey business is", inspections[0] * inspections[1])