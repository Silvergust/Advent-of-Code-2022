class Node:
	def __init__(self, height, name=None):
		self.height = "a" if height == "S" else "z" if height == "E" else height
		self.connected_nodes = []
		self.name = name

	def try_to_connect(self, other_node):
		#print("trying to connect {} with {}".format(self.name, other_node.name))
		if self.can_traverse(other_node):
			self.connected_nodes.append(other_node)
			#other_node.connected_nodes.append(self)
			#print(" - Connected!")
			#return
		if other_node.can_traverse(self):
			other_node.connected_nodes.append(self)
		#print(" - Failed!")

	def can_traverse(self, other_node):
		if (other_node == self):
			return False
		#if (abs(ord(self.height) - ord(other_node.height)) <= 1):
		if (ord(other_node.height) - ord(self.height) <= 1):
			return True
		return False

	def __repr__(self):
		return self.name if self.name != None else "Node ({})".format(self.height)

class BellmanFord:
	def __init__(self, nodes, start, goal):
		self.nodes = nodes
		self.start = start
		self.goal = goal
		self.min_distances = {}

	def process(self):
		for node in self.nodes:
			self.min_distances[node] = 9999
		self.min_distances[self.goal] = 0
		for i in range(len(self.nodes)+1):
			for node in self.nodes:
				for other_node in node.connected_nodes:
					if self.min_distances[node] > self.min_distances[other_node] + 1:
						self.min_distances[node] = self.min_distances[other_node] + 1
			#print("Relaxation step {} ended".format(i))



if __name__ == '__main__':
	file = open('input.txt','r')
	lines = file.read().splitlines()
	nodes_grid = []
	nodes = []
	print(lines)
	print(lines[0])

	start_node = None
	end_node = None
	for y in range(len(lines)):
		nodes_row = []
		lines_row = lines[y]
		#print("lines_row: ", lines_row)
		for x in range(len(lines_row)):
			node = Node(lines_row[x], name="({}, {})".format(x,y))
			nodes_row.append(node)
			#print("({},{})".format(x,y))
			#node.try_to_connect(nodes_grid[y][max(x-1,0)])
			nodes.append(node)
			if lines_row[x] == "S":
				start_node = node
			elif lines_row[x] == "E":
				end_node = node
		nodes_grid.append(nodes_row)
		#print(nodes_grid)
		for x in range(len(nodes_row)):
			#print("{},{}".format(x,y))
			nodes_row[x].try_to_connect(nodes_grid[y][max(x-1,0)])
			#print("x: ", x)
			nodes_row[x].try_to_connect(nodes_grid[max(y-1,0)][x])

	bf = BellmanFord(nodes, start_node, end_node)
	bf.process()

	#print("5,1:", nodes_grid[1][5].connected_nodes)
	for row in nodes_grid:
		dist_row = []
		for node in row:
			#print(node)
			#print("Connected: ", node.connected_nodes)
			#print(bf.min_distances[node])
			dist_row.append(bf.min_distances[node])
		print(dist_row)
	

	dict = {}
	for node in nodes:
		if bf.min_distances[node] not in dict:
			dict[bf.min_distances[node]] = set()
		print("Adding {} ({})".format(node, bf.min_distances[node]))
		dict[bf.min_distances[node]].add(node)

	for i in range(200):
		if i not in dict:
			break
		print("i - {}: {}".format(i, dict[i]))

	# path = [start_node]
	# current_node = start_node
	# while True:
	# 	if current_node == end_node:
	# 		break
	# 	for node in current_node.connected_nodes:
	# 		#print("{} -> {}?".format(bf.min_distances[current_node], bf.min_distances[node]))
	# 		if bf.min_distances[current_node] == bf.min_distances[node] + 1:
	# 			current_node = node
	# 			path.append(node)
	# 			break
	# #print("connected_nodes: ", start_node.connected_nodes)
	# print("Path: ", path)

	
	distances = []
	for row in nodes_grid:
		line = ""
		print("row length: ", len(row))
		i = 0
		for node in row:
			i += 1
			print("char: ", i)
			if node == end_node:
				line += "E!|"
				continue
			elif node == start_node:
				line += "S!|"
				continue
			line += (str(bf.min_distances[node]%100).zfill(2) + "|" if bf.min_distances[node] < 9000 else "..-")
		distances.append(line + "|\n")
		#print([ (bf.min_distances[node]%10 if bf.min_distances[node] < 9000 else ".") for node in row])

	print(distances)
	print("Dist: ", bf.min_distances[start_node])
	output = open('output.txt', 'w')
	output.writelines(distances)

	best_node = start_node
	for node in nodes:
		if node.height != "a":
			continue
		if bf.min_distances[node] < bf.min_distances[best_node]:
			best_node = node

	print("Best node: ", best_node)
	print("Distance: ", bf.min_distances[best_node])

