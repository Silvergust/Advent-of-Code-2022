file = open('input.txt', 'r')
lines = file.read().splitlines()

def get_value(item):
	o = ord(item)
	return (o - ord("A") + 27 if o < ord("a") else o - ord("a") + 1)

running_total = 0
#for line in lines:
for base_index in [3*n for n in range(len(lines)//3)]:
	#first_compartment = line[:len(line)//2]
	#second_compartment = line[len(line)//2:]
	first_compartment = lines[base_index]
	second_compartment = lines[base_index+1]
	third_compartment = lines[base_index+2]
	print(first_compartment)
	print(second_compartment)
	print(third_compartment)
	for item in first_compartment:
		if item in second_compartment and item in third_compartment:
			print("Duplicate item is ", item)
			print("Its value is ", get_value(item))
			running_total += get_value(item)
			print("Running total is ", running_total)
			break

print("Total value is ", running_total)