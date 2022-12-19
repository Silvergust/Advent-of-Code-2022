class Item:
	def __init__(self, worry):
		self.worry = worry

	def __repr__(self):
		return str(self.worry)

	def __lt__(self, other):
		return self.worry < other.worry

class Monkey:
	monkeys = []

	def __init__(self, item_worries, operation, test, true_target, false_target, divisor):
		self.items = [Item(worry) for worry in item_worries]
		#self.items.reverse()
		self.operation = operation
		self.test = test
		self.true_target = true_target
		self.false_target = false_target
		self.inspection_count = 0
		self.divisor = divisor
		Monkey.monkeys.append(self)

	def process_turn(self):
		#self.items.reverse()
		self.items.sort()
		while len(self.items) > 0:
			#item = self.items.pop()

			item = self.items[0]
			self.items = self.items[1:]
			#print("Monkey inspects an item with a worry level of ", item.worry)
			item.worry = self.operation(item.worry)
			#print("Worry level is now ", item.worry)
			#item.worry = item.worry // 3
			item.worry = item.worry % (2*3*5*7*11*13*17*19*23*27*29)
			#print("Monkey gets bored with item. Worry level is divided by 3 to ", item.worry)
			result = self.test(item.worry)
			#print("Current worry level {} test".format("passes" if result else "does not pass the"))
			self.inspection_count += 1
			self.throw(item, self.true_target if result else self.false_target)

	def throw(self, item, target_id):
		#print("Item with worry level {} is thrown to monkey {}".format(item.worry, target_id))
		item.worry = item.worry % (2*3*5*7*11*13*17*19*23*27*31)
		Monkey.monkeys[target_id].items.append(item)


if __name__ == '__main__':
	# file = open('test_input.txt', 'r')
	# #input = file.read(); #.splitlines()
	# monkeys = []
	# while True:
	# 	line = file.readline()
	# 	if line == "":
	# 		print("Finished parsing")
	# 		break

	# 	line = file.readline()
	# 	print("line: ", line)
	# 	items_string = line.split(": ")[1].split(", ")
	# 	items = [int(st) for st in items_string]
	# 	print("items: ", items)

	# 	line = file.readline()
	# 	print("line: ", line)
	# 	op_string, arg_string = line.split("new = old ")[1].split(" ")
	# 	print("op_string: ", op_string)
	# 	print("arg_string: ", arg_string)
	# 	print("Is *? ", op_string == "*")
	# 	if arg_string == "old\n":
	# 		operation = (lambda x: x * x) if op_string == "*" else (lambda x: x + x)
	# 	else:
	# 		arg = int(arg_string)
	# 		print("arg: ", arg)
	# 		operation = (lambda x: x * arg) if op_string == "*" else (lambda x: x + arg)
		
	# 	line = file.readline()
	# 	print("line: ", line)
	# 	div_string = line.split("by ")[1]
	# 	div = int(div_string)
	# 	print("div: ", div)
	# 	test = lambda x: x % div == 0

	# 	line = file.readline()
	# 	print("line: ", line)
	# 	true_string = line.split("monkey ")[1]
	# 	true_id = int(true_string)
	# 	print("true_id: ", true_id)

	# 	line = file.readline()
	# 	print("line: ", line)
	# 	false_string = line.split("monkey ")[1]
	# 	false_id = int(false_string)
	# 	print("false_id: ", false_id)

	# 	line = file.readline()
	# 	monkey = Monkey(items, operation, test, true_id, false_id)
	# 	monkeys.append(monkey)

	# print([monkey.items for monkey in monkeys])

	# monkey0 = Monkey([79, 98], lambda x: x*19, lambda x: x % 23 == 0, 2, 3)
	# monkey1 = Monkey([54, 65, 75, 74], lambda x: x+6, lambda x: x % 19 == 0, 2, 0)
	# monkey2 = Monkey([79, 60, 97], lambda x: x*x, lambda x: x % 13 == 0, 1, 3)
	# monkey3 = Monkey([74], lambda x: x+3, lambda x: x % 17 == 0, 0, 1)
	# monkeys = (monkey0, monkey1, monkey2, monkey3)

	monkey0 = Monkey([73, 77], lambda x: x*5, lambda x: x%11==0, 6, 5, 11)
	monkey1 = Monkey([57, 88, 80], lambda x: x+5, lambda x: x%19==0, 6, 0, 19)
	monkey2 = Monkey([61, 81, 84, 69, 77, 88], lambda x: x*19, lambda x: x%5==0, 3, 1, 5)
	monkey3 = Monkey([78, 89, 71, 60, 81, 84, 87, 75], lambda x: x+7, lambda x: x%3==0, 1, 0, 3)
	monkey4 = Monkey([60, 76, 90, 63, 86, 87, 89], lambda x: x+2, lambda x: x%13==0, 2, 7, 13)
	monkey5 = Monkey([88], lambda x: x+1, lambda x: x%17==0, 4, 7, 17)
	monkey6 = Monkey([84, 98, 78, 85], lambda x: x*x, lambda x: x%7==0, 5, 4, 7)
	monkey7 = Monkey([98, 89, 78, 73, 71], lambda x: x+4, lambda x: x%2==0, 3, 2, 2)
	monkeys = (monkey0, monkey1, monkey2, monkey3, monkey4, monkey5, monkey6, monkey7)

	#for x in range(5):
	#	print("f({}) = {}".format(x, monkeys[0].operation(x)))
	#a = 1/0

	round = 0
	while True:
		round += 1
		for monkey in monkeys:
			monkey.process_turn()
		#print("After round {}, the monkeys are holding items with these worry levels:".format(round))
		for i in range(len(monkeys)):
			#print("Monkey {}: {}".format(i, monkeys[i].items))
			pass
		#print([monkey.items for monkey in monkeys])
		#print([monkey.inspection_count for monkey in monkeys])
		if round >= 10000:
			break
	counts = [monkey.inspection_count for monkey in monkeys]
	print("Counts: ", counts)
	print("Max: ", max(counts))
	counts.sort()
	print("Result: ", counts[-1]*counts[-2])
	#print(sum(counts))
