file = open('input.txt', 'r')
#file = open('test_input.txt', 'r')
lines = file.read().splitlines()
#print(lines[:140])

running_total = 0
for line in lines:
	print(line)
	assignment_1, assignment_2 = line.split(',')
	range_1 = assignment_1.split('-')
	range_2 = assignment_2.split('-')
	set_1 = set( range(int(range_1[0]), int(range_1[1])+1))
	set_2 = set( range(int(range_2[0]), int(range_2[1])+1))
	intersection = set_1.intersection(set_2)
	#if ( (range_1[0] <= range_2[0] and range_2[1] <= range_1[1]) or range_2[0] <= range_1[0] and range_1[1]
	#print("{} <= {} <= {} <= {}".format(range_1[0], range_2[0], range_2[1], range_1[1]))
	#print(range_1[0] <= range_2[0])
	#print(range_2[0] <= range_2[1])
	#print(range_2[1] <= range_1[1])
	#if int(range_1[0]) <= int(range_2[0]) <= int(range_2[1]) <= int(range_1[1]) or int(range_2[0]) <= int(range_1[0]) <= int(range_1[1]) <= int(range_2[1]):
	#overlap_1 = len([n for n in [range(int(range_1[0]), int(range_1[1]))] if n in [range(int(range_2[0]), int(range_2[1]))]])
	#overlap_2 = len([n for n in [range(int(range_2[0]), int(range_2[1]))] if n in [range(int(range_1[0]), int(range_1[1]))]])
	#overlap = max(overlap_1, overlap_2)
	#overlap = len( [x for x in range( min( int(range_1[0]), int(range_2[0])), max( int(range_1[1]), int(range_2[1]))) if x in ] )
	#print("Overlap: ", overlap)
	if len(intersection) > 0:
		print("Intersection found!")
		running_total += 1

print("Total is ", running_total)