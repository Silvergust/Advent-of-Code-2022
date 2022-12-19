class Node:
	def __init__(self, parent=None, name="Node"):#, value=0):
		print("Adding node:")
		print(" - Parent: ", str(parent))
		print(" - Name: ", (name))
		#print(" - Value: ", (value))
		self.parent = None
		if (parent != None):
			self.attach_to_node(parent)
		if type(name) != type(""):
			print("Error: name is not a string!")
			a = 1/0
		self.name = name


	def add_child(self, child):
		if child not in self.children:
			self.children.append(child)

	def attach_to_node(self, parent):
		if (self.parent != None):
			self.parent.children.remove(self)
		self.parent = parent
		parent.children.append(self)

	def find_nodes(self, condition=lambda x: True):
		throw("Called Node proceedure.")
	# def get_value(self, condition= None):
	# 	total = self.value
	# 	for child in self.children:
	# 		total += child.get_value()
	# 	return total

	# def print_value(self, prefix, direct_only):
	# 	value = self.value if direct_only else self.get_value()
	# 	print(prefix + " " + str(self.name) + ": " + str(value)) # Inefficient
	# 	for child in self.children:
	# 		child.print_value(prefix + "-", direct_only)



class Directory(Node):
	def __init__(self, parent=None, name="Directory"):
		super().__init__(parent, name)
		self.children = []

	def get_value(self):
		total = 0
		for child in self.children:
			total += child.get_value()
		return total

	def print_value(self, prefix, direct_only):
		value = "(DIR)" if direct_only else self.get_value()
		print(prefix + " " + str(self.name) + ": " + str(value)) # Inefficient
		for child in self.children:
			child.print_value(prefix + "-", direct_only)

	def find_nodes(self, condition=lambda x: True):
		#if not condition(self):
		#	return []
		output = [self] if condition(self) else []
		for child in self.children:
			#if not type(child) == Directory:
			#	continue
			output.extend(child.find_nodes(condition))
		return output

	def find_subdirectories(self, condition=lambda x: True):
		return self.find_nodes(lambda x: (type(x) == Directory and condition(x)))


class File(Node):
	def __init__(self, parent=None, name="File", value=0):
		super().__init__(parent, name)
		print(" - Value: ", (value))
		if type(value) != type(4):
			print("Error: value is not an integer!")
			a = 1/0
		self.value = value

	def get_value(self, condition=None):
		return self.value

	def set_value(self, value):
		self.value = value

	def print_value(self, prefix, direct_only):
		print(prefix + str(self.value))

	def find_nodes(self, condition=lambda x: True):
		return [self] if condition(self) else []


class FileSystem:
	def __init__(self):
		self.root = Directory()
		self.current_node = self.root
		self.listing_files = False

	def parse_input(self, lines):
		for line in lines:
			print("line: ", line)
			fields = line.split(" ")
			print("Fields: ", fields)
			if fields[0] == "$":
				self.listing_files = False
				self.parse_command(fields)
			elif fields[0] == "dir":
				self.parse_add_directory(fields)
			elif fields[0].isdecimal():
				self.parse_file_data(fields)
			elif fields[0] == "exit": # For debugging purposes
				break
			elif fields[0][0] == "#":
				continue
			else:
				self.error("Parse input error in line "+ line)

	def parse_command(self, args):
		if args[1] == "cd":
			self.parse_cd(args[2])
		elif args[1] == "ls":
			self.listing_files = True
		else:
			self.error("Parse command error with arguments " + str(args))

	def parse_cd(self, arg):
		print("Parsing cd with argument: ", arg)
		if arg == "/":
			self.current_node = self.root
		elif arg == "..":
			self.current_node = self.current_node.parent
		else:
			self.current_node = self.find_node(arg)
		#else:
		#	error("Parse cd error with arguments: " + str(arg))

	def parse_add_directory(self, args):
		print("parse_add_directory with args ", str(args))
		print("Current_node: ", self.current_node)
		prev_node = self.find_node(args[1])
		if prev_node != None and type(prev_node) == Directory:
			print("Directory already present.")
			return
		node = Directory(self.current_node, args[1])
		#node.attach_to_node(self.current_node)

	def find_node(self, name):
		for child in self.current_node.children:
			if child.name == name:
				return child
		print("Child of name {} not found.".format(name))

	def parse_file_data(self, args):
		print("parse_file_data with arguments ", args)
		prev_node = self.find_node(args[1])
		if prev_node != None and type(prev_node) == File:
			print("Directory already present.")
			return
		node = File(self.current_node, args[1], int(args[0]))

	def error(self, error_string):
		print("ERROR: ", error_string)
		print("Root: ", self.root)
		print("Current node: ", self.current_node)
		a = 1/0


if __name__ == '__main__':
	file = open('input.txt','r')
	lines = file.read().splitlines()

	fs = FileSystem()
	fs.parse_input(lines)
	#fs.root.print_value("", True)
	fs.root.print_value("", False)
	print("Size: ", str(fs.root.get_value()))
	# for line in lines:
	# 	fields = line.split(" ")
	# 	if fields[0] == "$":
	# 		if fields[1] == "cd":
	# 			if fields[2] == "/":
	# 				current_node = root
	min_value = 0
	#checked_directories = [ (node.name, node.get_value()) for node in fs.root.find_subdirectories(lambda x: x.get_value() >= min_value and type(x) == Directory) ]
	checked_directories = [ (node.name, node.get_value()) for node in fs.root.find_subdirectories(lambda x: x.get_value() >= min_value)]
	#print(checked_directories)
	#print(sum([d[1] for d in checked_directories]))
	# smallest_usable_node = checked_directories[0]
	# min_value = 8381165
	# for node in checked_directories:
	# 	if node[1] < smallest_usable_node[1] and node[1] >= 8381165:
	# 		smallest_usable_node = node
	# print("smallest_node: ", smallest_usable_node)

	# subdirectories = fs.root.find_subdirectories()
	# subdirectories.sort(key=lambda x: x.get_value())
	# for sub in subdirectories:
	# 	print("{} : {}".format(sub.name, sub.get_value()))

	# smallest_subdirectory = subdirectories[0]
	# for sub in subdirectories:
	# 	if sub.get_value() < smallest_subdirectory.get_value() and sub.get_value() >= 7381165:
	# 		smallest_subdirectory = sub

	# print("Smallest sub: ({}, {})".format(smallest_subdirectory.name, smallest_subdirectory.get_value()))

	# print(fs.root.find_nodes())
	# names_dict = {}
	# for node in fs.root.find_nodes():
	# 	# if node.name in names_dict and type(node) in names_dict[node.name]:
	# 	# 	print("{} ({}) already in dict!".format(node.name, type(node)))
	# 	# 	break
	# 	if node.name not in names_dict:
	# 		names_dict[node.name] = { type(node) }
	# 	else:
	# 		names_dict[node.name] += type(node)

	subdirectories = fs.root.find_subdirectories()
	needed_space = 30000000 - (70000000 - subdirectories[0].get_value())
	smallest_sub = subdirectories[0]
	for sub in subdirectories:
		if needed_space <= sub.get_value() < smallest_sub.get_value():
			smallest_sub = sub

	print("needed_space: ", needed_space)
	print("{} : {}".format(smallest_sub.name, smallest_sub.get_value()))
	#print( [ (node.name, node.value) for node in fs.root.find_nodes(lambda x: True) if node.get_value >= 190])