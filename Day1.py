file = open("input.txt",'r')
st = file.read()
lines = st.split("\n")

max_calories = 0
current_calories = 0

class MaxList:
	def __init__(self):
		self.list = [0,0,0]
		self.min_index = 0

	def check_insert(self, value):
		if value > self.list[self.min_index]:
			print("Inserting ", value)
			self.list[self.min_index] = value
			self.update_min_index()

	def update_min_index(self):
		self.min_index = self.list.index(min(self.list))
		print("Min index is now ", self.min_index)

max_list = MaxList()

for line in lines:
	print("Line: ", line)
	if line == "":
		#max_calories = max(max_calories, current_calories)
		max_list.check_insert(current_calories)
		current_calories = 0
	else:
		current_calories += int(line)
		print("Current calories: ", current_calories)
#print("Max calories: ", max_calories)
print("Max calories: ", max_list.list)
print("Sum: ", sum(max_list.list))