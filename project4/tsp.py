# Project: #4 TSP
#
# Team RADZ:
#  Rittie Chuaprasert (chuaprar)
#  Austin Dubina (weila)
#  Darren Baker (bakerdar)
#  Zac Knudson (knudsoza)
# 
# CS 325-400
# Winter 2014

import sys, getopt, math, signal, atexit, time

cityList = []
cityCount = 0
visited = []
filename = ''
tourLength = 0
startCity = 15
intervals = 10

# The signal handler. On receiving sigterm, it writes
# the latest result to the file.
def sig_term():
	output()

#function to calculate the Euclidean distance between two cities
def calc_dist(x1,y1,x2,y2):
	if ((x1 == x2) and (y1 == y2)):
		return 0
	else:
		#round to the nearest integer. 
		#For 0.1, put a one, then for 0.01 put 2, etc. negative values work in the other direction
		return round(math.sqrt((x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2)),0)

# function to build the initial sub-optimal tour
def find_short_path(fromCity):
	global cityList
	global visited
	global cityCount
	minDist = 1000000
	tourCity = 0
	
	for toCity in range(cityCount):
		if (toCity not in set(visited)):
			thisDist = calc_dist(cityList[fromCity][0], cityList[fromCity][1], cityList[toCity][0], cityList[toCity][1])
			if (thisDist > 0 and thisDist < minDist):
				minDist = thisDist
				tourCity = toCity
	
	return tourCity

# function to output the visited tour file
def output()
	global visited
	global tourLength
	global filename
	fout = 0
	
	filename += '.tour' 

	fout = open(filename,'w')
	fout.write("%.0f\n" % tourLength)
	for city in visited:
		fout.write("{0}\n".format(city))
	
	fout.close()

# basic routine to optimize tour length by cycling through a number of 2-opt swaps and array reversals
def optimize_tour():
	global visited
	global tourLength

	tour_size = len(visited)
	prev_tour_length = 0

	for cycle in range(20):
		if (tour_size == cityCount):
			print "------------------------- CYCLE", cycle, "------------------------------"
		visited.reverse()
		for i in range(2, tour_size-1):
			if (i % 250 == 0):
				print "======= TOUR STOP", i, "of", tour_size-1, "========="
				tour_distance_check()
			for j in range(i, tour_size-1):
				opt_swap(visited[i-2], visited[i-1], visited[j], visited[j+1])

		if (tour_size == cityCount):
			tour_distance_check()
			if (tourLength == prev_tour_length):
				break
			prev_tour_length = tourLength

# calculates the tour length given the current visited[] array.  Outputs city count and tour length.
def tour_distance_check():
	global visited
	global tourLength

	thisDistance = 0
	cumDistance = 0

	# distance from starting city to all other cities
	for x in range(1, len(visited)):
		thisDistance = calc_dist(cityList[visited[x-1]][0], cityList[visited[x-1]][1], cityList[visited[x]][0], cityList[visited[x]][1])
		cumDistance += thisDistance

	# distance back to first city
	thisDistance = calc_dist(cityList[visited[x]][0], cityList[visited[x]][1], cityList[visited[0]][0], cityList[visited[0]][1])
	cumDistance += thisDistance

	print "#cities:", len(visited), "Length:", cumDistance
	tourLength = cumDistance

# calculates the tour length given the current visited[] array.  Outputs city count and tour length.
# Additional output includes all cities, coordinates, and incremental/cumulative distances of the tour.
def tour_distance_check_detail():
	global visited
	global tourLength

	thisDistance = 0
	cumDistance = 0

	# check figures: cities and main program tourLength
	print "\n#cities:", len(visited), "Length:", tourLength

	# first city - this is the tour starting point
	print 0, cityList[visited[0]][0], cityList[visited[0]][1], cityList[visited[0]][2]

	# distance from starting city to all other cities
	for x in range(1, len(visited)):
		thisDistance = calc_dist(cityList[visited[x-1]][1], cityList[visited[x-1]][2], cityList[visited[x]][1], cityList[visited[x]][2])
		cumDistance += thisDistance
		print x, cityList[visited[x]][0], cityList[visited[x]][1], cityList[visited[x]][2], "dist:", thisDistance, "cum dist:", cumDistance

	# distance back to first city
	thisDistance = calc_dist(cityList[visited[x]][1], cityList[visited[x]][2], cityList[visited[0]][1], cityList[visited[0]][2])
	cumDistance += thisDistance
	print 0, cityList[visited[0]][0], cityList[visited[0]][1], cityList[visited[0]][2], "dist:", thisDistance, "cum dist:", cumDistance

	print "#cities:", len(visited), "Length:", cumDistance
	tourLength = cumDistance


# @param A, B, C, D:	indexes within visited[] representing 4 tour cities
# precondition: arguments are 4 distinct cities, represent 2 pairs of adjacent tour cities in a valid tour in the order they appear within the tour.
# postcondition: if AB+CD > AC+BD, tour is adjusted for shorter distances; otherwise, no change to tour. 
#	=> edges AB and CD are removed; edges AC and BD are added to tour. Original path B..C is reversed within tour.
def opt_swap(A, B, C, D):
	global visited

	orig_edge1 = calc_dist(cityList[A][0], cityList[A][1], cityList[B][0], cityList[B][1])
	orig_edge2 = calc_dist(cityList[C][0], cityList[C][1], cityList[D][0], cityList[D][1])
	new_edge1  = calc_dist(cityList[A][0], cityList[A][1], cityList[C][0], cityList[C][1])
	new_edge2  = calc_dist(cityList[B][0], cityList[B][1], cityList[D][0], cityList[D][1])
	if (orig_edge1 + orig_edge2 > new_edge1 + new_edge2):
		print "********** swapping [", A, B, "] and [", C, D,"] **********"
		#print "AB:", orig_edge1, "CD:", orig_edge2, "total:", orig_edge1 + orig_edge2 
		#print "AC:", new_edge1, "BD:", new_edge2, "total:", new_edge1 + new_edge2 
		idxB = visited.index(B)
		idxD = visited.index(D)
		slice_beg = visited[:idxB]
		slice_mid = visited[idxB:idxD]
		slice_end = visited[idxD:]
		#print slice_beg, slice_mid, slice_end
		slice_mid.reverse()
		visited = slice_beg + slice_mid + slice_end
		#print visited

		tour_distance_check()

# procedure to parse the input file, initialize the visited array, and optimize the tour
def find_tour():
	global filename
	global cityList
	global cityCount
	global visited
	global tourLength
	global startCity
	global intervals
	distance = 0
	tourCity = 0
	x_max = 0
	y_max = 0
	x_min = 100000000
	y_min = 100000000
	x_step = 0
	y_step = 0
	x_idx = 0
	y_idx = 0	
	
	mini_vis = [[0 for x in xrange(intervals*intervals)] for x in xrange(1000)]

	with open(filename) as f:
		for line in f:
			cityList.append(map(int, line.strip().split()[1:3]))

	#get the count of cities
	cityCount = len(cityList)

	# get x and y max and min
	for i in range(cityCount):
		if (cityList[i][0] > x_max):
			x_max = cityList[i][0]
		elif (cityList[i][0] < x_min):
			x_min = cityList[i][0]

		if (cityList[i][1] > y_max):
			y_max = cityList[i][1]
		elif (cityList[i][1]) < y_min:
			y_min = cityList[i][1]
		#visited.append(i)

	print x_min, x_max, y_min, y_max, "cityCount:", cityCount
	x_step = (x_max - x_min)/intervals + 1
	y_step = (y_max - y_min)/intervals + 1
	
	for i in range(intervals):
		for j in range(intervals):
			mini_vis[i*intervals + j] = []

	for i in range(cityCount):
		x_idx = (cityList[i][0] - x_min) / x_step
		y_idx = (cityList[i][1] - y_min) / y_step
		#print x_idx, y_idx		
		mini_vis[x_idx*intervals + y_idx].append(i)

	for i in range(intervals):
		for j in range(intervals):
			print i, j, "count:", len(mini_vis[i*intervals + j])
			#print mini_vis[i*intervals + j]

	# determine the order of the tour as it hops mini-segments
	tour_order = []
	curr_idx = 0
	for i in range(intervals):
		tour_order += [i*intervals]

	curr_idx = intervals * (intervals-1)
	for i in range(intervals-1):
		curr_idx += 1
		tour_order += [curr_idx]

	curr_idx -= intervals

	for loop in range(intervals/2 - 1):
		tour_order += [curr_idx]
		for i in range(intervals-2):
			curr_idx -= intervals
			tour_order += [curr_idx]

		curr_idx -= 1
		tour_order += [curr_idx]
		for i in range(intervals-2):
			curr_idx += intervals
			tour_order += [curr_idx]

		curr_idx -= 1
		print curr_idx, tour_order

	tour_order += [curr_idx]
	for i in range(intervals-2):
		curr_idx -= intervals
		tour_order += [curr_idx]

	"""
	tour_order = [0,10,20,30,40,50,60,70,80,90,91,92,93,94,95,96,97,98,99]
	tour_order += [89,79,69,59,49,39,29,19,9]
	tour_order += [8,18,28,38,48,58,68,78,88]
	tour_order += [87,77,67,57,47,37,27,17,7]
	tour_order += [6,16,26,36,46,56,66,76,86]
	tour_order += [85,75,65,55,45,35,25,15,5]
	tour_order += [4,14,24,34,44,54,64,74,84]
	tour_order += [83,73,63,53,43,33,23,13,3]
	tour_order += [2,12,22,32,42,52,62,72,82]
	tour_order += [81,71,61,51,41,31,21,11,1]
	"""
	print tour_order

	# optimize the mini-arrays
	for i in range(intervals):
		for j in range(intervals):
			if (len(mini_vis[i]) > 3):
				visited = mini_vis[i*intervals + j]
				print i, j, len(mini_vis[i*intervals + j]), visited
				optimize_tour()
				mini_vis[i*intervals + j] = visited

	visited = []
	for i in range(len(tour_order)):
		visited += mini_vis[tour_order[i]]

	print visited

	"""
	#go on a tour {note: at this stage, starting city 15 is optimal for sample1; city 165 is optimal for sample2}
	if (startCity > cityCount):
		startCity = 0
	tourCity = startCity
	visited.append(tourCity)
	for c in range(cityCount - 1):
		tourCity = find_short_path(tourCity)
		visited.append(tourCity)
	"""

	#-----added by Rittie----------------------------------------------
	#for x in range(cityCount):
	#	print cityList[x][0], cityList[x][1], cityList[x][2]

	#tour_distance_check_detail()
	optimize_tour()
	tour_distance_check()
	#------------------------------------------------------------------

	# write output to file
	output()

def main(argv):
	global filename
	
	# Register signal handler
    signal.signal(signal.SIGTERM, sig_term)
	
	opts, args = getopt.getopt(argv, "hf:", ["filename="])	
	
	for o, a in opts:
		if o == '-h':
			print 'usage: tsp.py -f <filename>'
			sys.exit()
		elif o in ("-f", "--filename"):
			filename = a
		else:
			assert False, "unhandled option"	

	find_tour()

if __name__ == '__main__':
	main(sys.argv[1:])
