def sign(value):
	return 1 if value > 0 else 0 if value == 0 else -1

class RopeSegment:
	def __init__(self, parent):
		self.pos = [0,0]
		self.parent = parent
		if (self.parent):
			self.parent.child = self
		self.visited_locs = []

	def move(self, vector):
		if not parent:
			self.head_pos[0] += vector[0]
			self.head_pos[1] += vector[1]
			return

	#print("Head moved {}, its coordinates are now {}".format(vector, self.head_pos))
		for index in [0,1]:
			#print("diff[{}]: {}".format(index, self.head_pos[index] - self.tail_pos[index]))
			if abs(self.head_pos[index] - self.tail_pos[index]) >= 2:
				tail_move_vector = [None, None]
				#self.tail_pos[0] = self.head_pos[0] + sign(self.tail_pos[0] - self.head_pos[0])
				#self.tail_pos[1] = self.head_pos[1] + sign(self.tail_pos[1] - self.head_pos[1])
				tail_move_vector[0] = - sign(self.tail_pos[0] - self.head_pos[0])
				tail_move_vector[1] = - sign(self.tail_pos[1] - self.head_pos[1])
				#self.tail_pos[0] = self.head_pos[0] + tail_move_vector[0]
				#self.tail_pos[1] = self.head_pos[1] + tail_move_vector[1]
				self.tail_pos[0] += tail_move_vector[0]
				self.tail_pos[1] += tail_move_vector[1]
				#print("Tail move vector: ", tail_move_vector)
				#print("Tail moved, its coordinates are now {}".format(self.tail_pos))
		
		#print("Head moved {}, its coordinates are now H:{} ; T:{}".format(vector, self.head_pos, self.tail_pos))
		if str(self.tail_pos) not in self.visited_locs:
			#self.visited_locs.add(self.head_pos)
			#print("Appending {} to list of visited tail locations".format(self.tail_pos))
			self.visited_locs.append(str(self.tail_pos))

			if self.child:
				self.child.move_and_update([0,0])

class RopeMap:
	def __init__(self):
		self.head_pos = [0,0]
		self.tail_pos = [0,0]
		

	


	def parse(self, line):
		print("parsing line: ", line)
		direction, amount_string = line.split(" ")
		vector = (0,1) if direction == "U" else (0,-1) if direction == "D" else (-1,0) if direction == "L" else (1,0)
		for i in range(int(amount_string)):
			self.move(vector)

if __name__ == '__main__':
	file = open('input.txt', 'r')
	lines = file.read().splitlines()
	rm = RopeMap()
	for line in lines:
		rm.parse(line)
	print(rm.visited_locs)
	print(len(rm.visited_locs))