# Solve Day 11, Puzzle 1
# https://adventofcode.com/2022/day/10

# D11P1_input.txt provides a list of monkeys who are throwing some of your 
# missing stuff around, as well as the rules by which the monkeys decide where
# to throw those items.

# GOAL: Determine which two monkeys inspect the most items after 1000 rounds. 
# Submit the level of monkey business (the product of numbers of inspections).
# Also, this time worry levels are not reduced after items are inspected.

# Notes: My first answer (32399460002) was too high. Taking the modulus of the
# product of all test ints (9699690) -- as opposed to just the test int for the 
# next monkey -- solved the problem.

################################################################################

class Monkey:

    def __init__(self, item_list, op_symbol, op_int, test_int, 
                 throw_index_true, throw_index_false, monkey_id):
        self.starting_items = item_list
        self.operator = op_symbol
        self.operation_int = op_int
        self.test = test_int
        self.throw_when_true = throw_index_true
        self.throw_when_false = throw_index_false
        self.id = monkey_id
        self.inspection_tally = 0

    def ThrowItems(self, monkey_list):

        # print("Monkey", self.id, "items:", self.starting_items)
        
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

            # monkey tests worry level and throws item
            # input lists all tests as checking divisibility by provided int
            if (item_after_inspection % self.test) == 0:
                next_monkey = monkey_list[self.throw_when_true]
            else:
                next_monkey = monkey_list[self.throw_when_false]

            # 9699690 is the product of all the monkeys' test ints
            finalized_item = (item_after_inspection % 9699690)
            next_monkey.starting_items.append(finalized_item)

        # remove items from the monkey's list of items
        self.starting_items.clear()

################################################################################

# Because there are only 8 monkeys, it's easier to manually make them all
# (as opposed to parsing the input file)
monkey0 = Monkey([85, 79, 63, 72], "*", 17, 2, 2, 6, 0)
monkey1 = Monkey([53, 94, 65, 81, 93, 73, 57, 92], "**", 2, 7, 0, 2, 1)
monkey2 = Monkey([62, 63], "+", 7, 13, 7, 6, 2)
monkey3 = Monkey([57, 92, 56], "+", 4, 5, 4, 5, 3)
monkey4 = Monkey([67], "+", 5, 3, 1, 5, 4)
monkey5 = Monkey([85, 56, 66, 72, 57, 99], "+", 6, 19, 1, 0, 5)
monkey6 = Monkey([86, 65, 98, 97, 69], "*", 13, 11, 3, 7, 6)
monkey7 = Monkey([87, 68, 92, 66, 91, 50, 68], "+", 2, 17, 4, 3, 7)

monkeys = [monkey0, monkey1, monkey2, monkey3, monkey4, monkey5, monkey6, monkey7]



# simulate 20 rounds of monkeys throwing items
round = 0
while round < 10000:

    print("Starting round", round)

    for monkey in monkeys:
        monkey.ThrowItems(monkeys)

    round += 1

# create a sorted list (descending order) for number of times each monkey inspected
inspections = []
for monkey in monkeys:
    inspections.append(monkey.inspection_tally)

inspections.sort(reverse=True)

print("")
print(inspections)
print("The level of monkey business is", inspections[0] * inspections[1])