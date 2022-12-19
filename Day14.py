class Sand:
	def __init__(self):
		#self.x = 500
		#self.y = 0
		self.coords = [500, 0]

	def __repr__(self):
		#return "({}, {})".format(self.x, self.y)
		return str(self.coords)

class Cave:
	def __init__(self):
		#self.coords = [500, 0]
		self.finished = False
		self.max_depth = 0
		self.min_left = 9999999
		self.rocks = []
		self.sands = []
		self.sand_coords = []
		self.rock_coords = set()
		self.sand_coords = set()
		#self.sands_at_rest = 0

	def create_line(self, start, end):
		if start[0] == end[0]:
			const_coord = 0
			var_coord = 1
		else:
			const_coord = 1
			var_coord = 0
		for i in range(min(start[var_coord], end[var_coord]), max(start[var_coord], end[var_coord])+1):
			#print("Adding rock ")
			rock = [None, None]
			rock[const_coord] = start[const_coord]
			rock[var_coord] = i
			#self.rocks.append((start[const_coord], i))
			print("Adding rock ", rock)
			self.rocks.append(rock)
			self.rock_coords.add((rock[0],rock[1]))
		if self.max_depth < max(start[1], end[1]):
			self.max_depth = max(start[1], end[1])
		if self.min_left > min(start[0], end[0]) - 1:
			self.min_left = min(start[0], end[0]) - 1

	def is_available(self, coords):
		#print("Coords: ", coords)
		#return self.rocks[coords[1]][coords[0]] == None
		# if coords in self.rocks:
		# 	#print("is_available() found a rock")
		# 	return False
		# for sand in self.sands:
		# 	#print("is_available() found sand")
		# 	if coords == sand.coords:
		# 		return False
		if coords in self.rock_coords or coords in self.sand_coords:
			return False
		if coords[1] >= 2 + self.max_depth:
			#print("Reached the bottom")
			return False
		#print("is_available() found nothing")
		return True

	def create_sand(self):
		sand = Sand()
		self.process(sand)

	def process(self, sand):
		#sand_coords = [500, 0]
		print("Sand is currently at ", sand.coords)
		print(len(self.sands))
		while True:
			# if sand.coords[1] > self.max_depth:
			# 	print("Sand fell down the pit at ", sand.coords)
			# 	self.finished = True
			# 	break

			#print("sand.coords: ", sand.coords)
			#print("sand.coords[0]: ", sand.coords[0])
			#print("sand.coords[1]: ", sand.coords[1])
			#print("(sand.coords[0], sand.coords[1]+1): ", (sand.coords[0], sand.coords[1]+1))
			if self.is_available((sand.coords[0], sand.coords[1]+1)):
				sand.coords[1] += 1
				#print("Sand felled one step.")
			elif self.is_available((sand.coords[0]-1, sand.coords[1]+1)):
				sand.coords[0] -= 1
				sand.coords[1] += 1
				#print("Sand moved to the left.")
			elif self.is_available((sand.coords[0]+1, sand.coords[1]+1)):
				sand.coords[0] += 1
				sand.coords[1] += 1
				#print("Sand moved to the right.")
			else:
				#print("Sand came to rest at ", sand.coords)
				self.sands.append(sand)
				self.sand_coords.add((sand.coords[0], sand.coords[1]))
				if sand.coords == [500,0]:
					self.finished = True
				break
			#self.process(sand)
		

	def __repr__(self):
		# map = []
		# for y in range(self.max_depth):
		# 	row = ""
		# 	for x in range(self.min_left, self.min_left + 20):
		# 		row .append(".")
		# 	map.append(row)
		# for rock in self.rocks:
		# 	map[rock[1]][rock[0]] = "#"
		# for sand in self.sands:
		# 	map[rock[1]][rock[0]] = "o"
		map = [ [None]*20 for row in range(self.max_depth+3)]
		#print(map)
		print("Min left: ", self.min_left)
		for rock in self.rocks:
			#print("Rock: ", rock)
			if rock[0] <= len(map[0]):
				map[rock[1]][rock[0] - self.min_left] = "#"
		for sand in self.sands:
			#map[rock[1]][rock[0] - self.min_left] = "o"
			map[sand.coords[1]][sand.coords[0] - self.min_left] = "o"
		output = []
		for y in range(len(map)):
			row = ""
			for x in range(len(map[0])):
				#if map[y][x] == None:
				#	map[y][x] = "."
				row += "." if map[y][x] == None else map[y][x]
			output.append(row)
		return str(output)



file = open("input.txt", 'r')
input_lines = file.read().splitlines()

cave = Cave()
for line in input_lines:
	input_coords = line.split(" -> ")
	for i in range(len(input_coords)-1):
		print(input_coords[i])
		x1,y1 = [int(value) for value in input_coords[i].split(",")]
		x2,y2 = [int(value) for value in input_coords[i+1].split(",")]
		#x2,y2 = int(coords[i+1].split(","))
		print("x1: {} | y1: {} | x2: {} | y2: {}".format(x1,y1,x2,y2))
		cave.create_line((x1, y1), (x2, y2))
print("Rocks:")
print(cave.rocks)
while not cave.finished:
	cave.create_sand()
print("Rocks:")
print(cave.rocks)
print("Sands:")
print(cave.sands)
print("Sands at rest: ", len(cave.sands))
print(cave)
print("Sands at rest: ", len(cave.sands))