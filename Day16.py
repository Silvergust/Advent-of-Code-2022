import sys
import typing
import itertools

test = False
simplify = False
t_frequency = 100000
#current_valve_pruning = True
#current_valve_pruning_delta = 200

class Tunnel:
	def __init__(self, start_valve : typing.Self, end_valve: typing.Self, cost: int):
		self.start_valve = start_valve
		self.end_valve = end_valve
		self.cost = cost

	def __repr__(self) -> str:
		return "{}->{} ({})".format(self.start_valve, self.end_valve, self.cost)

class Valve:
	def __init__(self, name: str, flow_rate: int):
		self.name = name
		self.flow_rate = flow_rate
		self.available_tunnels = []

	def get_available_tunnels(self) -> list[Tunnel]:
		return self.available_tunnels

	#def set_available_tunnels(self, tunnels):
#		self.available_tunnels = tunnels

	def add_tunnel(self, end_valve: typing.Self, cost: int, simplify: bool=True) -> None:
		# if end_valve.flow_rate == 0 and simplify:
		# 	# for tunnel in end_valve.available_tunnels:
		# 	# 	for t in tunnel.end_valve.available_tunnels:
		# 	# 		if t.end_valve != self and tunnel.cost + t.cost > cost:
		# 	# 			self.add_tunnel(self, t, tunnel.cost + t.cost)
		# 	for tunnel in end_valve.available_tunnels:
		# 		if tunnel.end_valve != self and tunnel.cost + 1 > cost:
		# 			self.add_tunnel(tunnel.end_valve, tunnel.cost + 1, simplify)
		# else:
		# 	self.available_tunnels.append(Tunnel(self, end_valve, cost))
		self.available_tunnels.append(Tunnel(self, end_valve, cost))

	def try_to_simplify(self, prev_valve : typing.Self, next_valve : typing.Self):
		did_simplify = False
		if self.flow_rate > 0:
			return False
		for prev_tunnel in prev_valve.available_tunnels[:]:
			for next_tunnel in next_valve.available_tunnels[:]:
				if prev_tunnel.end_valve == self and next_valve in [t.end_valve for t in self.available_tunnels] and prev_valve != next_valve:
					#print("prev_valve.available_tunnels: ", prev_valve.available_tunnels)
					#print("prev_tunnel: ", prev_tunnel)
					print("{}->{}->{} simplified".format(prev_valve, self, next_valve))
					prev_valve.available_tunnels.remove(prev_tunnel)
					next_valve.available_tunnels.remove(next_tunnel)
					prev_valve.add_tunnel(next_valve, prev_tunnel.cost+next_tunnel.cost)
					did_simplify = True
					break
			if did_simplify:
				break
		return did_simplify

	def can_traverse(self, other_valve : typing.Self):
		for tunnel in self.available_tunnels:
			if tunnel.end_valve == other_valve:
				return True, tunnel.cost
		return False, -1

	def get_traverse_cost(self, other_valve : typing.Self):
		for tunnel in self.available_tunnels:
			if tunnel.end_valve == other_valve:
				return tunnel.cost
		raise Exception("Tunnel from {} to {} not found. Available tunnels are {}".format(self, other_valve, self.available_tunnels))

	# def simplify(self):
	# 	new_tunneling = self.available_tunnels[:]
	# 	for tunnel in self.available_tunnels:
	# 		if tunnel.flow_rate > 0:
	# 			print("{}'s flow rate is greater than 0.".format(tunnel))
	# 			continue
	# 		new_tunneling.remove(tunnel)
	# 		print("available_tunnels: ", tunnel.available_tunnels)
	# 		for valve in tunnel.available_tunnels:
	# 			print(" - {}".format(valve))
	# 			if valve != self:
	# 				print("Appending tunnel ".format(tunnel))
	# 				new_tunneling.append(valve)
	# 			else:
	# 				print("{} is the checked valve.".format(valve))
	# 	for valve in new_tunneling:
	# 		print("Valve: ", valve)
	# 		if valve not in self.available_tunnels:
	# 			self.available_tunnels = new_tunneling
	# 			print("Valve {} simplified to {}.".format(self, self.available_tunnels))
	# 			self.simplify()
	# 			break
	# 	print("Stopped simplification, new_tunneling is {} while previous tunneling is {}".format(new_tunneling, self.available_tunnels))

	# def simplify(self, ignore=[]):
	# 	new_tunneling = self.available_tunnels[:]
	# 	simplified = False
	# 	for tunnel in self.available_tunnels[:]:
	# 		if tunnel.flow_rate > 0 :
	# 			continue
	# 		print(tunnel.available_tunnels)
	# 		#new_tunneling.remove(tunnel)
	# 		new_tunneling.remove(tunnel)
	# 		new_tunneling.extend( [ t for t in tunnel.available_tunnels if t != self and t not in ignore])
	# 		ignore.append(tunnel)
	# 		simplified = True
	# 	self.available_tunnels = new_tunneling[:]
	# 	print("Available tunneling is now ", self.available_tunnels)
	# 	if simplified:
	# 		print("Simplifying again")
	# 		self.simplify(ignore)

	def __repr__(self) -> str:
		return self.name

Instruction = typing.Union[str, Valve]

class Analyzer:
	# def __init__(self):
	# 	self.last_instructions = []

	def evaluate(instructions : list[Instruction]):
		open_valves = set()
		current_valve = Analyzer.default_valve
		current_pressure = 0
		max_time = 30
		if len(instructions) >= max_time+1:
			return -1, False
		#print("instructions: ", instructions)
		#for t in range(max_time):
		traversing_delay = 0
		t = 0
		inst_index = 0
		while t < max_time:
			total_flow_rate = sum([valve.flow_rate for valve in open_valves])
			current_pressure += total_flow_rate
			#print("Valves {} are open, releasing {} pressure.\n".format(open_valves, current_pressure))
			t += 1
			#print("== Minute {} ==".format(t+1))
			if traversing_delay > 0:
				traversing_delay -= 1
			
			if inst_index < len(instructions):
				#print("Instruction: ", instructions[t])
				#print("t: {}, instructions[{}]: {}".format(t, inst_index, instructions[inst_index]))
				
				if type(instructions[inst_index]) == Valve:
					traversing_delay += current_valve.get_traverse_cost(instructions[inst_index]) - 1
					current_valve = instructions[inst_index]
					inst_index += 1
					continue
				else:
					if current_valve in open_valves: # Probably worse than not checking
						#print("Valve already open")
						return -1, False
					elif current_valve.flow_rate == 0:
						print("Valve has 0 flow rate")
						return -1, False
					else:
						open_valves.add(current_valve)
						inst_index += 1
						#current_pressure += (max_time - t) * current_valve.flow_rate
						#print("Opened {}, maximum pressure will now be {}".format(current_valve, current_pressure))
						#print("There are now {} open valves".format(len(open_valves)))
		#print("Current_pressure: ", current_pressure)
		#print("Analyzer.ideal_pressures[current_valve]: ", Analyzer.ideal_pressures[current_valve])
		all_open = len(open_valves) >= Analyzer.max_open_valves
		# if not current_valve_pruning:
		# 	return current_pressure, all_open
		if Analyzer.ideal_pressures[current_valve][0] > current_pressure and Analyzer.ideal_pressures[current_valve][1] > total_flow_rate:
			#print("Instructions {} discarded due to redundancy. Pressure was {} (previous was {}), flow was {} (previous was {})".format(instructions, current_pressure, Analyzer.ideal_pressures[current_valve][0], total_flow_rate, Analyzer.ideal_pressures[current_valve][1]))
			return -1, False
		else:
			Analyzer.ideal_pressures[current_valve][0] = current_pressure
			Analyzer.ideal_pressures[current_valve][1] = total_flow_rate
			return current_pressure, all_open

	def get_current_valve(instructions : list[Instruction]) -> Valve:
		#print("Getting valve from ", instructions)
		# for i in reversed(range(len(instruction))):
		# 	print("i: ", i)
		# 	print(instructions[:-1-i])
		# 	if type(instructions[:-1-i]) == Valve:
		# 		print("Returning ", instructions[:-1-i])
		# 		return instructions[:-1-i]
		for inst in reversed(instructions):
			if type(inst) == Valve:
				#print("Returning", inst)
				return inst
		#if len(instructions) == 0:
		#	return Analyzer.default_valve
		#return Analyzer.default_valve
		raise Exception("Current valve not found for instruction! Instructions were: ", instructions)
		#return Analyzer.default_valve

	def test(instructions, expected_result):
		result = Analyzer.evaluate(instructions)
		assert result[0] == expected_result, "Assertion expected ´{}, obtained {} instead. Analyzer's last instructions were {}.".format(expected_result, result[0], instructions)

class Queue:
	def __init__(self):
		self.items = []
		self.index = 0

	def enqueue(self, item: Instruction):
		self.items.append(item)

	def dequeue(self) -> Instruction:
		self.index += 1
		#print("Queue is currently {} and next index is {}. Dequeueing".format(self, self.index))
		return self.items[self.index-1]

	def cull(self):
		pass

	def __len__(self) -> int:
		return len(self.items) - self.index

	def __repr__(self) -> str:
		# if len(self.items) <= 5:
		# 	return str(self.items[self.index:])
		# else:
		# 	return str(self.items[self.index : self.index + 6])
		#return str(self.items[self.index:]) if len(self.items) <= 5 else str(self.items[self.index : self.index+6]) + " and other " + len(self.items) - self.index
		return str(self.items[self.index:]) if len(self.items) <= 5 else "{} and other {} items".format(self.items[self.index : self.index+6], len(self.items) - self.index)

if __name__ == '__main__':
	file = open(str(sys.argv[1]) if len(sys.argv) > 1 else "input.txt", 'r')
	lines = file.read().splitlines()
	tunnel_strings_dict = {}
	valves_list = []
	Analyzer.default_valve = None
	Analyzer.ideal_pressures = {}
	#starting_instructions = [["open"]]
	#starting_instructions = [] # Assuming AA always has flow_rate 0
	nonzero_flow_count = 0
	names_to_valves_dict = {}
	def n2v(name):
		return names_to_valves_dict[name]
	for line in lines:
		print("Line: ", line)
		name = line.split(" ")[1]
		print(name)
		flow_rate = int( line.split(" ")[4].split("=")[1][:-1] )
		valve = Valve(name, flow_rate)
		print("default: ", Analyzer.default_valve)
		if valve.name == "AA":
			Analyzer.default_valve = valve
			#print("Set {} as the default valve.".format(Analyzer.default_valve))
		names_to_valves_dict[valve.name] = valve
		#if valve.name in ["DD", "BB", "II"]:
		#if valve.name in ["BV", "ZE", "PE", "XL"]:
		#	starting_instructions.append([valve])
		if valve.flow_rate > 0:
			nonzero_flow_count += 1
		valves_list.append(valve)
		Analyzer.ideal_pressures[valve] = [-1,-1]
		if line.split("valve")[1][0] == "s":
			tunnel_strings_dict[valve] = line.split("valves ")[1]
		else:
			tunnels_st = line.split("valve ")[1]
			tunnel_strings_dict[valve] = tunnels_st.split(", ")
		#print(tunnels_st)
		#tunnel_strings_dict[valve] = line.split("valve ")[1]
		#tunnel_strings_dict[valve] = tunnels_st.split()
	print(valves_list)
	print(tunnel_strings_dict)
	for valve in tunnel_strings_dict.keys():
		tunnels_strings = tunnel_strings_dict[valve]
		print("{}: {}".format(valve, tunnels_strings))
		for candidate_for_tunnel in valves_list:
			if candidate_for_tunnel.name in tunnels_strings:
				#valve.available_tunnels.append(candidate_for_tunnel)
				valve.add_tunnel(candidate_for_tunnel, 1, simplify)
				print("Appended ", candidate_for_tunnel)
			else:
				#print(candidate_for_tunnel, "Not in string")
				pass
		print(" Valve {} has flow rate={}; tunnels lead to valves {}".format(valve.name, valve.flow_rate, valve.get_available_tunnels()))
		#print(" Valve {} has flow rate={}; tunnels lead to valves {}".format(valve.name, valve.flow_rate, valve.available_tunnels))
	Analyzer.max_open_valves = nonzero_flow_count

	simplify_succeeded = False
	count = 0
	#for i in range(len(valves_list)):
	if simplify:
		while True:
			print("Attempting to simplify")
			simplify_succeeded = False
			for v1, v2, v3 in itertools.product(valves_list, valves_list, valves_list):
				if v2.try_to_simplify(v1, v3):
					simplify_succeeded = True
				#print("Tried to simplify {}->{}->{} and {}.".format(v1, v2, v3, "succeeded" if simplify_succeeded else "failed"))
				count += 1
				#if count % 351 == 0:
				#	print("{}: {}, {}, {}".format(count, v1, v2, v3))

			if not simplify_succeeded:
				break
			else:
				print("Did simplify")


		for valve in valves_list:
			#valve.simplify()
			print("{} : {}".format(valve, valve.get_available_tunnels()))
		#n2v("AA").simplify()
		print("Tunnels connected to AA: ", n2v("AA").available_tunnels)


	starting_instructions = [ [tunnel.end_valve] for tunnel in n2v("AA").available_tunnels ]
	# 	print("{} : {}".format(valve, valve.available_tunnels))
	# 	assert ( len(valve.get_available_tunnels()) == len(valve.available_tunnels))
	# 	for i in range(len(valve.get_available_tunnels())):
	# 		valve.get_available_tunnels()[i] == valve.available_tunnels[i]
	#a = 1/0

	# Analyzer.ideal_pressures[aa] = -1
	# Analyzer.ideal_pressures[bb] = -1
	# Analyzer.ideal_pressures[cc] = -1
	# Analyzer.ideal_pressures[dd] = -1
	# Analyzer.ideal_pressures[ee] = -1
	# Analyzer.ideal_pressures[ff] = -1
	# Analyzer.ideal_pressures[gg] = -1
	# Analyzer.ideal_pressures[hh] = -1
	# Analyzer.ideal_pressures[ii] = -1
	# Analyzer.ideal_pressures[jj] = -1

	#print(Analyzer.evaluate([dd, "open", cc, "open"])[0])
	#print(Analyzer.evaluate([dd, "open"]))
	#print(Analyzer.evaluate([bb, "open"]))
	#print(Analyzer.evaluate([dd, aa, dd, "open"]))
	#print(Analyzer.evaluate([dd, 'open', cc, bb, 'open', aa, ii, jj, 'open', ii, aa, dd, ee, ff, gg, hh, 'open', gg, ff, ee, 'open', dd, cc, 'open']))
	#print(Analyzer.evaluate([dd, cc, 'open']))
	#print(Analyzer.evaluate([dd, "open", cc, 'open']))
	#print(Analyzer.evaluate(['open']))
	#print(Analyzer.evaluate([dd, cc, dd, cc, dd, 'open']))
	#print(Analyzer.evaluate([dd, 'open', cc, bb, 'open', aa, ii, jj, 'open']))

	analyzer = Analyzer()
	 
	if test:
		if not simplify:
	# # For test input
			aa = n2v("AA")
			bb = n2v("BB")
			cc = n2v("CC")
			dd = n2v("DD")
			ee = n2v("EE")
			ff = n2v("FF")
			gg = n2v("GG")
			hh = n2v("HH")
			ii = n2v("II")
			jj = n2v("JJ")
			Analyzer.test([bb, "open"], 364)
			Analyzer.test([dd, "open"], 560)
			Analyzer.test([dd, "open", cc, 'open'], 612)
			Analyzer.test([dd, "open", cc, bb, "open", aa, ii, jj, "open", ii, aa, dd, ee, ff, gg, hh, "open", gg, ff, ee, "open", dd, cc, "open"], 1651)
			# test_result = Analyzer.evaluate([bb, "open"])
			# assert test_result[0] == 364, "obtained {} instead.".format(test_result)
			# test_result = Analyzer.evaluate([dd, "open"])
			# assert test_result[0] == 560, "obtained {} instead.".format(test_result)
			# test_result = Analyzer.evaluate([dd, "open", cc, 'open'])
			# assert test_result[0] == 612, "obtained {} instead.".format(test_result)
			 #test_result = Analyzer.evaluate([dd, "open", cc, bb, "open", aa, ii, jj, "open", ii, aa, dd, ee, ff, gg, hh, "open", gg, ff, ee, "open", dd, cc, "open"])
			Analyzer.test([dd, "open", cc, bb, "open", aa, ii, jj, "open", ii, aa, dd, ee, ff, gg, hh, "open", gg, ff, ee, "open", dd, cc, "open"], 1651)
			#print(Analyzer.evaluate([dd, "open", cc, bb, "open", aa, ii, jj, "open", ii, aa, dd, ee, ff, gg, hh, "open", gg, ff, ee, "open", dd, cc, "open"]))
			Analyzer.test([ii, jj, "open"], 567)
			Analyzer.test([bb, 'open', aa, ii, jj, 'open', ii, aa, dd, 'open', ee, ff, gg, hh, 'open', gg, ff, ee, 'open', dd, cc, 'open'])
			print(Analyzer.evaluate([bb, 'open', aa, ii, jj, 'open', ii, aa, dd, 'open', ee, ff, gg, hh, 'open', gg, ff, ee, 'open', dd, cc, 'open']))
			#Analyzer.test([dd, "open", cc, bb, "open"])

		#a = 1/0
		# test_result = Analyzer.evaluate([n2v("II"), n2v("JJ"), "open"])
		# assert(test_result[0] == 567)
		# test_result = Analyzer.evaluate([n2v("DD"), "open", n2v("CC"), n2v("BB"), "open", n2v("AA"), n2v("II"), n2v("JJ"), "open", n2v("II"), n2v("AA"), n2v("DD"), n2v("EE"), n2v("FF"), n2v("GG"), n2v("HH"), "open", n2v("GG"), n2v("FF"), n2v("EE"), "open", n2v("DD"), n2v("CC"), "open"])
		# assert(test_result[0] == 1651)

		# test_result = Analyzer.evaluate(["open", n2v["BV"], "open", n2v["KK"], n2v["TU"], "open", n2v["MG"], n2v["CS"], n2v["OZ"], "open"])
		# print(test_result[0])
		# assert(test_result[0] == -1)
		# test_result = Analyzer.evaluate([n2v["BV"], n2v["KK"], n2v["TU"], "open", n2v["MG"], n2v["CS"], n2v["OZ"], "open"])
		# # raise Exception("End of tests")
		# print(test_result[0])
		# assert(test_result[0] == 402)

	print("starting_instructions: ", starting_instructions)
	queue = Queue()
	for inst in starting_instructions:
		queue.enqueue(inst)
	#Analyzer.default_valve = aa
	#queue.enqueue(["open"])
	#queue.enqueue([dd])
	#queue.enqueue([ii])
	#queue.enqueue([bb])
	#queue.enqueue([])
	#for inst in starting_instructions:
#		queue.enqueue(inst)
	best_instructions = []
	best_value = 0
	t = 0
	print(queue)

	print("\n\n ##### SEARCHING #####\n\n")
	while len(queue) > 0:
		if t % t_frequency == 0:
			print("t: ", t)
			print("Queue is now ", queue)
		#if t >= 20:
	#		break
		t += 1
		if len(queue) == 0:
			break
		instruction = queue.dequeue()
		#if len(instruction) > 5:
		#	continue
		#print("Dequeued ", instruction)
		val, all_open = Analyzer.evaluate(instruction)
		#print("Pressure is ", val)
		if val < 0:
			#print("Worthless instruction")
			continue
		if best_value < val:
			best_value = val
			best_instructions = instruction
			print("Better instruction found! {} pressure for {}".format(val, instruction))
		if all_open:
			print("Instructions {} open all valves, no point looking further.".format(instruction))
			#continue
			pass
		new_instruction = instruction[:]	
		new_instruction.append("open")
		queue.enqueue(new_instruction)
		current_valve = Analyzer.get_current_valve(instruction)
		#print("current_valve: ", current_valve)
		for tunnel in current_valve.get_available_tunnels():
			#print("Valve: ", valve)
			new_instruction = instruction[:]
			new_instruction.append(tunnel.end_valve)
			queue.enqueue(new_instruction)
		#print("Queue is now ", queue)
		#print("Queue length is now ", len(queue))

# Unfortunately the code does not return the correct value
print("Best pressure is {} for instructions {}".format(best_value, best_instructions))
print("default_valve: ", Analyzer.default_valve, )
print("Max open valves: ", Analyzer.max_open_valves)
print("Starting instructions: ", starting_instructions)
