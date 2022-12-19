def sign(value):
	return 1 if value > 0 else 0 if value == 0 else -1

class RopeSegment:
	def __init__(self, parent):
		self.pos = [0,0]
		self.parent = parent
		self.child = None
		if (self.parent):
			self.parent.child = self
		self.visited_locs = []

	def move(self, vector):
		if not self.parent:
			self.pos[0] += vector[0]
			self.pos[1] += vector[1]
			if self.child:
				self.child.move([0,0])
			return

	#print("Head moved {}, its coordinates are now {}".format(vector, self.head_pos))
		for index in [0,1]:
			#print("diff[{}]: {}".format(index, self.head_pos[index] - self.tail_pos[index]))
			if abs(self.parent.pos[index] - self.pos[index]) >= 2:
				tail_move_vector = [None, None]
				#self.tail_pos[0] = self.head_pos[0] + sign(self.tail_pos[0] - self.head_pos[0])
				#self.tail_pos[1] = self.head_pos[1] + sign(self.tail_pos[1] - self.head_pos[1])
				tail_move_vector[0] = - sign(self.pos[0] - self.parent.pos[0])
				tail_move_vector[1] = - sign(self.pos[1] - self.parent.pos[1])
				#self.tail_pos[0] = self.head_pos[0] + tail_move_vector[0]
				#self.tail_pos[1] = self.head_pos[1] + tail_move_vector[1]
				self.pos[0] += tail_move_vector[0]
				self.pos[1] += tail_move_vector[1]
				#print("Tail move vector: ", tail_move_vector)
				#print("Tail moved, its coordinates are now {}".format(self.tail_pos))
		
		#print("Head moved {}, its coordinates are now H:{} ; T:{}".format(vector, self.head_pos, self.tail_pos))
		if str(self.pos) not in self.visited_locs:
			#self.visited_locs.add(self.head_pos)
			#print("Appending {} to list of visited tail locations".format(self.tail_pos))
			self.visited_locs.append(str(self.pos))

		if self.child:
			self.child.move([0,0])

class Rope:
	def __init__(self, length):
		self.segments = [RopeSegment(None)]
		for i in range(1,length):
			self.segments.append(RopeSegment(self.segments[i-1]))

	def parse(self, line):
		print("parsing line: ", line)
		direction, amount_string = line.split(" ")
		vector = (0,1) if direction == "U" else (0,-1) if direction == "D" else (-1,0) if direction == "L" else (1,0)
		for i in range(int(amount_string)):
			self.segments[0].move(vector)
			#for j in range(len(self.segments)):
			#	print("Segment {} is now at {}".format(j, self.segments[j].pos))

if __name__ == '__main__':
	file = open('input.txt', 'r')
	lines = file.read().splitlines()
	length = 10
	rope = Rope(length)
	for line in lines:
		if line == " ":
			break
		rope.parse(line)

		# for j in range(15,-15, -1):
		# 	row = ""
		# 	for i in range(-15,15):
		# 		#print([i,j])
		# 		#print([str(seg.pos) for seg in rope.segments])
		# 		row += "#" if str([i,j]) in [str(seg.pos) for seg in rope.segments] else "."
		# 	print(row)

	print(rope.segments[length-1].visited_locs)
	print(len(rope.segments[length-1].visited_locs))