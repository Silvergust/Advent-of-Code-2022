class TreeGrid:
	def __self__(self):
		self.grid = []
		self.width = None
		self.height = None

	def parse_grid(self, filename):
		file = open(filename,'r')
		lines = file.read().splitlines()

		self.width = len(lines[0])
		self.height = len(lines)
		self.grid = []
		for y in range(self.height):
			self.grid.append([])
			for x in range(self.width):
				self.grid[y].append(lines[y][x])

	def is_visible(self, x, y):
		self.row = self.grid[y]
		self.column = [row[x] for row in self.grid]
		height = self.grid[y][x]
		#print("row: ", self.row)
		#print("column: ", self.column)
		#print("height: ", height)
		
		# for i in range(self.width):
		# 	if not ( 0 < i < self.width-1 and i != x):
		# 		continue
		# 	for j in range(self.height):
		# 		if not ( 0 < i < self.height-1 and j != y):
		# 			continue
		# 		if self.grid[j][i] >= self.grid[y][x]:
		# 			#print("Tree at {},{} is not visible".format(x,y))
		# 			return False


		for j in range(0, y):
			#print("j: {}, grid[j][x]: {}".format(j, self.grid[j][x]))
			if self.grid[j][x] >= self.grid[y][x]:
				break
		else:
			#print("Tree at {},{} is visible from the top".format(x,y))
			return True

		for j in range(y+1, self.height):
			#print("j: {}, grid[j][x]: {}".format(j, self.grid[j][x]))
			if self.grid[j][x] >= self.grid[y][x]:
				break
		else:
			#print("Tree at {},{} is visible from the bottom".format(x,y))
			return True

		for i in range(0, x):
			#print("i: {}, grid[y][i]: {}".format(i, self.grid[y][i]))
			if self.grid[y][i] >= self.grid[y][x]:
				break
		else:
			#print("Tree at {},{} is visible from the left".format(x,y))
			return True

		for i in range(x+1, self.width):
			#print("i: {}, grid[y][i]: {}".format(i, self.grid[y][i]))
			if self.grid[y][i] >= self.grid[y][x]:
				break
		else:
			#print("Tree at {},{} is visible from the right".format(x,y))
			return True
		return False

	def calculate_visibility(self, x, y):
		top = [ int(self.grid[j][x]) for j in range(y-1, -1, -1)]
		bottom = [ int(self.grid[j][x]) for j in range(y+1, self.height)]
		left = [ int(self.grid[y][i]) for i in range(x-1, -1,-1)]
		right = [ int(self.grid[y][i]) for i in range(x+1, self.width)]
		height = int(self.grid[y][x])
		top_value = limit_count(top, height)
		bottom_value = limit_count(bottom, height)
		left_value = limit_count(left, height)
		right_value = limit_count(right, height)
		# print("top_value: ", top_value)
		# print("bottom_value: ", bottom_value)
		# print("left_value: ", left_value)
		# print("right_value: ", right_value)
		return top_value*bottom_value*left_value*right_value

def limit_count(list, limit):
	running_total = 0
	for item in list:
		running_total += 1
		if item >= limit:
			break
	return running_total


if __name__ == '__main__':
	tg = TreeGrid()
	tg.parse_grid("input.txt")
	#print(tg.grid)
	#print([[tg.is_visible(x, y) for x in range(tg.width)] for y in range(tg.height)])
	#print(sum([ sum([ tg.is_visible(x, y) for x in range(tg.width)]) for y in range(tg.height)]))
	print( max( [ max([tg.calculate_visibility(x, y) for x in range(tg.width)]) for y in range(tg.height)]))
	#print(tg.calculate_visibility(2,1))
