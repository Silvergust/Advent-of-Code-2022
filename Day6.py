file = open('input.txt', 'r')
message = file.read()

#running_total = 0
for index in range(14,len(message)):
	substring = message[index-14:index]
	#print("substring: ", substring)
	found = False
	for char in substring:
		#print("Checking char ", char)
		if substring.count(char) > 1:
			#print(char, " is repeated.")
			found = True
		if found:
			break
	if not found:
		print("Found 14 unique characters at index {}, substring {}".format(index, substring))


#print("running_total: ", running_total)