class ChoicesEnum:
	a = 0
	x = 0
	b = 1
	y = 1
	c = 2
	z = 2


def result_score(opponents_choice, my_choice):
	diff = opponents_choice - my_choice
	if diff in [-1, 2]:
		print("I won")
		return 6
	elif diff == 0:
		print("Draw")
		return 3
	else:
		print("I lost")
		return 0

# result_score_dict = {
# 	ChoicesEnum.x : 0,
# 	ChoicesEnum.y : 3,
# 	ChoicesEnum.z : 6 
# }

# def updated_result_score(my_choice):
# 	return ChoicesEnum[my_choice]

choice_score_dict = {
	ChoicesEnum.a : 1,
	ChoicesEnum.x : 1,
	ChoicesEnum.b : 2,
	ChoicesEnum.y : 2,
	ChoicesEnum.c : 3,
	ChoicesEnum.z : 3
}


def choice_score(choice):
	return choice_score_dict[choice]

def updated_choice_score(opponents_choice, result):
	result_score = 0
	my_choice = None
	if result == ChoicesEnum.x:
		if opponents_choice == ChoicesEnum.a:
			my_choice = ChoicesEnum.c
		elif opponents_choice == ChoicesEnum.b:
			my_choice = ChoicesEnum.a
		elif opponents_choice == ChoicesEnum.c:
			my_choice = ChoicesEnum.b
		else:
			raise ("55 Error!")
	elif result == ChoicesEnum.y:
		result_score = 3
		my_choice = opponents_choice
	elif result == ChoicesEnum.z:
		result_score = 6
		if opponents_choice == ChoicesEnum.a:
			my_choice = ChoicesEnum.b
		elif opponents_choice == ChoicesEnum.b:
			my_choice = ChoicesEnum.c
		elif opponents_choice == ChoicesEnum.c:
			my_choice = ChoicesEnum.a
		else:
			raise ("67 Error!")
	else:
		raise("69 Error!")
	return result_score + choice_score_dict[my_choice]



string_enum_dict = {
	"A" : ChoicesEnum.a,
	"X" : ChoicesEnum.x,
	"B" : ChoicesEnum.b,
	"Y" : ChoicesEnum.y,
	"C" : ChoicesEnum.c,
	"Z": ChoicesEnum.z
}

def parse_line(line):
	opponents_choice, my_choice = line.split(" ")
	opponents_choice = string_enum_dict[opponents_choice]
	my_choice = string_enum_dict[my_choice]
	return [opponents_choice, my_choice]

file = open("input.txt", 'r')
st = file.read()

lines = st.split('\n')
total_score = 0
for line in lines:
	print("Line: ", line)
	if line == "":
		break
	opponents_choice, my_choice = parse_line(line) #line.split(" ")
	#score = result_score(opponents_choice, my_choice)
	#score += choice_score(my_choice)
	score = updated_choice_score(opponents_choice, my_choice)
	print("Got ", score, " points")
	total_score += score
	print("Running total: ", total_score)
print("Final score: ", total_score)