first = "first"
equal = "equal"
last = "last"

def compare(this, that):
	#print("Comparing {} vs {}".format(this, that))
	if type(this) == type(5) and type(that) == type(5):
		return first if this < that else equal if this == that else last
	elif type(this) == list and type(that) == list:
		for i in range(min(len(this), len(that))):
			if compare(this[i], that[i]) == equal:
				continue
			elif compare(this[i], that[i]) == first:
				#print("compare(this[i], that[i]) == first")
				return first
			elif compare(this[i], that[i]) == last:
				#print("compare(this[i], that[i]) == last")
				return last
			print("This: ", this)
			print("That: ", that)
			raise Exception("Failed to compare at index ", i)
		if len(this) < len(that):
			#print("len(this) < len(that)")
			return first
		elif len(this) > len(that):
			#print("len(this) > len(that)")
			return last
		elif len(this) == len(that):
			#print("len(this) == len(that):")
			return equal
		else:
			print("This: ", this)
			print("That: ", that)
			raise Exception("Failed to tiebreak")
	elif type(this) == list and type(that) == type(5):
		return compare(this, [that])
	elif type(this) == type(5) and type(that) == list:
		return compare([this], that)
	else:
		#print("This: ", this)
		#print("That: ", that)
		raise Exception("Invalid typing")

# if __name__ == '__main__':
# 	file = open('input.txt', 'r')

# 	correct_indices = []
# 	i = 1
# 	while True:
# 		#if i >= 20:
# 		#	break
# 		print("\nPair ", i)
# 		line_1 = file.readline()
# 		line_2 = file.readline()
# 		blank_line = file.readline()
# 		data_1 = eval(line_1)
# 		data_2 = eval(line_2)
# 		print(data_1)
# 		print(data_2)
# 		#packet_1 = Packet(data_1)
# 		#packet_2 = Packet(data_2)
# 		#comparison = packet_1 <= packet_2
# 		comparison = compare(data_1, data_2)
# 		print(comparison)
# 		if comparison == None:
# 			print("None error")
# 		if comparison == first:
# 			correct_indices.append(i)
		
# 		i += 1
# 		if blank_line == "":
# 			break
class PacketContainer:
	def __init__(self, packet):
		self.packet = packet

	def __lt__(self, other):
		return compare(self.packet, other.packet) == first

	def __eq__(self, other):
		return compare(self.packet, other.packet) == equal

	def __repr__(self):
		return str(self.packet)

if __name__ == '__main__':
	file = open("input.txt", 'r')
	lines = file.read().splitlines()
	packets = [PacketContainer(eval(line)) for line in lines if line != ""]
	packets.append(PacketContainer([[2]]))
	packets.append(PacketContainer([[6]]))
	packets.sort()
	print(packets[:20])
	print("Index 1: ", 1+packets.index(PacketContainer([[2]])))
	print("Index 2: ", 1+packets.index(PacketContainer([[6]])))

#print(correct_indices)
#print(sum(correct_indices))