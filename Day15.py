import time
class Item:
	def __init__(self, coords):
		self.coords = coords
		self.attached = None
		#if beacon_coords != None:
		#	self.detected_item = Item(beacon_coords)

	def attach_item(self, other_item):
		self.attached = other_item
		self.distance = abs(self.coords[0] - self.attached.coords[0]) + abs(self.coords[1] - self.attached.coords[1])


	def get_boundary(self):
		output = []
		distance = self.distance + 1
		t = time.time()
		# for i in range(distance):
		# 	output.append( (self.coords[0] - distance + i, self.coords[1] + i) )
		# 	output.append( (self.coords[0] + i, self.coords[1] + distance - i) )
		# 	output.append( (self.coords[0] + distance - i, self.coords[1] - i) )
		# 	output.append( (self.coords[0] - i, self.coords[1] - distance + i) )
		output.extend( [ (self.coords[0] - distance + i, self.coords[1] + i) for i in range(distance)] )
		output.extend( [ (self.coords[0] + i, self.coords[1] + distance - i) for i in range(distance)] )
		output.extend( [ (self.coords[0] + distance - i, self.coords[1] - i) for i in range(distance)] )
		output.extend( [ (self.coords[0] - i, self.coords[1] - distance + i) for i in range(distance)] )
		print(time.time() - t)
		return output



	def __repr__(self):
		return str( (self.coords[0], self.coords[1]) )

class Map:
	def __init__(self):
		self.min = -2000000
		self.max = 8000000
		self.sensors = set()
		self.beacons = set()

	def add_sensor(self, sensor_coords, beacon_coords):
		sensor = Item(sensor_coords)
		beacon = Item(beacon_coords)
		sensor.attach_item(beacon)
		self.sensors.add(sensor)
		self.beacons.add(beacon)

	def add_beacon(self, coords):
		self.beacon_coords.add(Item(coords))

	def analyze_row(self, row_index, minimum = -99999999, maximum = 99999999):
		row = ["."]*(self.max - self.min + 1)
		for sensor in self.sensors:
			distance = (abs(sensor.coords[0] - sensor.attached.coords[0]) + abs(sensor.coords[1] - sensor.attached.coords[1]))
			delta_y = abs(sensor.coords[1] - row_index)
			width = distance - delta_y

			# if -self.min + sensor.coords[0] - width < 0:
			# 	#print("ERROR: scan exceeded leftmost limit.")
			# 	#print("Sensor: ", sensor)
			# 	#continue
			# 	pass
			# if -self.min + sensor.coords[0] + width >= self.max - self.min:
			# 	#print("ERROR: scan exceeded rightmost limit.")
			# 	#print("Sensor: ", sensor)
			# 	#continue
			# 	pass

			for discarded_index in range(max(self.min, sensor.coords[0] - self.min - width), min(self.max - self.min, sensor.coords[0] - self.min + width)+1):
				row[discarded_index] = "#"

			if delta_y == 0 and self.min <= sensor.coords[0] <= self.max:
				row[-self.min + sensor.coords[0]] = "S"
			if row_index == sensor.attached.coords[1] and self.min <= sensor.attached.coords[0] <= self.max:
				row[-self.min + sensor.attached.coords[0]] = "B"

		#return row
		output = f'{row_index:3}' + ": "
		for char in row:
			output += char
		return output

	def analyze_map(self, start_row, end_row):
		#self.discarded = set()
		self.discarded = {}
		for i in range(self.min, self.max+1):
			#print(j)
			self.discarded[i] = set()
			for j in range(start_row, end_row+1):
			#	#self.discarded.add( (i, j))
				self.discarded[i].add(j)

		#print("self.discarded: ")
		#print(self.discarded)
		for sensor in self.sensors:
			distance = abs(sensor.coords[0] - sensor.attached.coords[0]) + abs(sensor.coords[1] - sensor.attached.coords[1])
			j_range = range(max(start_row, sensor.coords[1] - distance), min(end_row, sensor.coords[1] + distance) + 1)
			for j in j_range:
				#print(j_range)
				i_range = range(max(self.min, sensor.coords[0] - distance), min(self.max, sensor.coords[0] + distance) + 1)
				for i in i_range:
					if i == 14 and j == 11:
						print("Incorrect discard caused by sensor: ", sensor)
						print("i_range: {} ( {}-{} )".format(i_range, sensor.coords[0] - distance, sensor.coords[0] + distance))
						print("j_range: {} ( {}-{} )".format(j_range, sensor.coords[1] - distance, sensor.coords[1] + distance))
						print("distance: ", distance)
					self.discarded[i].discard(j)

		# for d in self.discarded.keys():
		# 	if len(self.discarded[d]) == 0:
		# 		self.discarded.pop(d)

	def get_minimum_distance_delta(self, x, y):
		minimum_delta = 99999999
		min_sensor = None
		for sensor in self.sensors:
			distance = abs(sensor.coords[0] - x) + abs(sensor.coords[1] - y)
			#minimum_distance = min(minimum_distance, distance)
			if minimum_distance > distance :
				minimum_distance = distance
				min_sensor = sensor
		return minimum_distance, min_sensor

	def scan(self, x_min, x_max, y_min, y_max):
		memo_dict = set()
		boundary = []
		for sensor in self.sensors:
			#boundary = sensor.get_boundary()
			print ("Adding boundary for sensor ", sensor)
			boundary.extend([ coord for coord in sensor.get_boundary() if x_min <= coord[0] <= x_max and y_min <= coord[1] <= y_max ])
		count = 0
		for coords in boundary:
			if coords in memo_dict:
				continue
			memo_dict.add(coords)
			# distance = abs(sensor.coords[0] - coords[0]) + abs(sensor.coords[1] - coords[1])
			# #if distance <= sensor.distance:
			# #	continue
			# min_distance = self.get_minimum_distance(coords[0], coords[1])
			# if min_distance > 0:
			# 	return coords
			count += 1
			if count % 1000 == 0:
				print("Count: {}/{}".format(count, len(coords)))
			#print("Checking coords ", coords)
			for sensor in self.sensors:
				#print( " -- Checking sensor ", sensor)
				distance = abs(sensor.coords[0] - coords[0]) + abs(sensor.coords[1] - coords[1])
				if distance <= sensor.distance:
					break
			else:
				#print("Beacon found! It's at ", coords)
				return coords






if __name__ == '__main__':
	file = open('input.txt', 'r')
	lines = file.read().splitlines()
	map = Map()
	for line in lines:
		print("line: ", line)
		sx = int(line.split(" ")[2].split("=")[1][:-1])
		sy = int(line.split(" ")[3].split("=")[1][:-1])
		bx = int(line.split(" ")[8].split("=")[1][:-1])
		by = int(line.split(" ")[9].split("=")[1])
		print("sx: {}, sy: {}, bx: {}, by: {}".format(sx, sy, bx, by))
		map.add_sensor((sx, sy), (bx, by))
	print("Sensors: ", map.sensors)
	print("Beacons: ", map.beacons)
		#map.add_sensor((bx, by))
	map.min = -4
	#map.max = 20
	map.max = 60
	#for i in (range(-4, 40)):
	# 	print(map.analyze_row(i))
	print("Scan:")
	print(map.scan(0,4000000,0,4000000))
	#def test_distance(x, y):
	#	print("({}, {}), minimum distance is {} (from sensor {})".format(x, y, map.get_minimum_distance(x, y)[0], map.get_minimum_distance(x, y)[1]))
	#test_distance(11, 14)
	#test_distance(12, 14)
	#test_distance(0,0)
	#test_distance(6,0)
	#test_distance(14,11)
	# 	row = map.analyze_row(i)
	# 	if "." in row:
	# 		print("Dot found!")
	# 		index = row.index(".")
	# 		print("i: ", i)
	# 		print("index: ", i)
	# 		print("Location: ({}, {})".format(index, i))
	# 		print("Frequency: ", str(4000000*index + i))
	#for sensor in map.sensors:
	#	print(sensor.get_boundary())
	#	print(len(sensor.get_boundary()))
	# map.analyze_map(0, 20)
	# #print(map.discarded)
	# for key in map.discarded:
	# 	if len(map.discarded) > 0:
	# 		print("({}, {})".format(key, map.discarded[key]))
	# row = map.analyze_row(2000000)
	# #row = map.analyze_row(10)
	# count = 0
	
	# for i in range(len(row)):
	# 	#print(row[i])
	# 	if row[i] == "#":
	# 		count += 1
	# print(count)
