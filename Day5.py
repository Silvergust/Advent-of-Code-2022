file = open('input.txt', 'r')
lines = file.read().splitlines()

# Initialize stacks
line_index = 0
stacks = []
for i in range(1 + len(lines[0])//4):
	stacks.append([])
print("Stacks length: ", len(stacks))
print("Stacks: ", stacks)

# Read input and fill stacks
for line in lines:
	print("line: ", line)
	column = 0
	if line[1].isalpha() or line[1] == " ":
		for i in range(1,len(line),4):
			stacks[column].append(line[i])
			print("Appending {} to stack {}.".format(line[i], column))
			print("Column {} is now: {}".format(column, stacks[column]))
			column += 1
	elif line[1] == "1":
		print("End of stacks found.")
		line_index += 2
		break
	line_index += 1

# Clean up stacks data
stack_index = 0
for stack in stacks:
	stack.reverse()
	stack_index += 1
	while stack[-1] == " ":
		stack.pop()
	print("Stack {} is: {}".format(stack_index, stack))

# Perform move operations
while True:
	if line_index >= len(lines):
		break
	print("Line: ", lines[line_index])
	line_breakdown = lines[line_index].split(" ")
	for index in [1, 3, 5]:
		if not line_breakdown[index].isdigit():
			print("Error on line ", lines[line_index])
			break
	index_of_stack_to_move_from = int(line_breakdown[3])-1
	index_of_stack_to_move_to = int(line_breakdown[5])-1
	amount = int(line_breakdown[1])
	moved_boxes = []
	for i in range(amount):
		moved_boxes.append(stacks[index_of_stack_to_move_from].pop())
		#print("Moving box ", box)
		#stacks[index_of_stack_to_move_to].append(box)
		#print("Stack {} now looks like: {}".format(index_of_stack_to_move_to, stacks[index_of_stack_to_move_to]))
		#print("Index error on line index ", line_index)
	moved_boxes.reverse()
	print("Moving boxes ", moved_boxes)
	stacks[index_of_stack_to_move_to].extend(moved_boxes)
	print("Stack {} now looks like: {}".format(index_of_stack_to_move_to, stacks[index_of_stack_to_move_to]))

	line_index += 1

print("Final stacking:")
print(stacks)

top_boxes = []
for stack in stacks:
	top_boxes.append(stack.pop() if len(stack) >= 1 else " ")

print("Top boxes: ", top_boxes)
output_string = ""
for box in top_boxes:
	output_string += box

print("output_string: ", output_string)