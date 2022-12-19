class Register:
	stop = "Stop"

	def __init__(self, input_lines):
		self.cycle = 1
		self.current_process = None
		self.value = 1
		self.noop = Noop(self)
		self.addx = Addx(self)
		self.input_lines = input_lines
		self.input_lines.reverse()
		self.finished = False
		self.pixel = "."


	def update(self):
		self.print("update()")
		if self.finished:
			self.print("Register already finished")
			return
		self.print("Current process is " + str(self.current_process))

		# if self.current_process != None:
		# 	response = self.current_process.update_process()
		# 	if response == Register.stop:
		# 		self.print("Process ended")
		# 		self.current_process = None
		# 		self.parse(self.input_lines.pop())
		# else:
		# 	self.parse(self.input_lines.pop())
		if self.current_process == None:
			self.parse(self.input_lines.pop())
		response = self.current_process.update_process()
		#print("response: ", response)
		if response == Register.stop:
			#print("Stopping.")
			self.current_process = None

		self.set_pixel()
		self.cycle += 1

		if len(self.input_lines) == 0:
			self.finished = True


	def parse(self, line):
		self.print("Parsing line " + line)
		if line == "noop":
			self.print("Read noop")
			self.current_process = self.noop
			self.noop.start()
			return
		lines = line.split(" ")
		addx_value = int(lines[1])
		self.print("Read addx with value: " + str(addx_value))
		self.current_process = self.addx
		self.addx.start(addx_value)

	def print(self, st):
		#print("{}: {}".format(self.cycle, st))
		pass

	def print2(self, st):
		print("{}: {}".format(self.cycle, st))

	def set_pixel(self):
		x = self.cycle % 40
		result = "#" if self.value - 1 <= x <= self.value + 1 else "."
		self.print2("{}, thus setting it to {}".format(self.value, result))
		self.pixel = result

	def get_pixel(self):
		return self.pixel

class Process:
	def __init__(self, parent):
		self.parent = parent
		self.duration = self.cost

	def start(self):
		self.duration = self.cost

	def update_process(self):
		self.duration -= 1
		#print("duration: ", self.duration)
		if self.duration == 0:
			self.print(str(self) + " reached its end.")
			return self.update_func()

	def update_func(self):
		raise("Update_func() called on base Process.")

	def print(self, st):
		self.parent.print(st)


class Noop(Process):
	def __init__(self, parent):
		self.cost = 1 # Has to go before super so that it knows what to set self.duration to
		super().__init__(parent)
		

	def update_func(self):
		return Register.stop

	def __repr__(self):
		return "Noop"

class Addx(Process):
	def __init__(self, parent):
		self.cost = 2
		super().__init__(parent)
		self.value = None

	def start(self, value):
		super().start()
		self.value = value

	def update_func(self):
		#print("value: {}, parent value: {}".format(self.value, self.parent.value))
		self.parent.value += self.value
		self.print("Register value is now " + str(self.parent.value) + " <-------")
		return Register.stop

	def __repr__(self):
		return "Addx " + str(self.value)


if __name__ == '__main__':
	file = open('input.txt', 'r')
	input_lines = file.read().splitlines()
	register = Register(input_lines)
	values = []
	strengths = []
	image = []
	while True:
		row = ""
		for x in range(40):
			register.update()
			row += register.get_pixel()
			if (register.cycle + 20) % 40 == 0:
				print("### Cycle: ", register.cycle)
				print("### Value is ", register.value)
				values.append(register.value)
				strengths.append(register.cycle * register.value)
			if register.finished:
				break
		image.append(row)
		if register.finished:
			break
print("values: ", values)
print("strengths: ", strengths)
print(sum(strengths))
print(image)