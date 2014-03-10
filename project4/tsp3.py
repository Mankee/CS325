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

bestTour = []
bestLength = 1000000000
cityList = []
cityCount = 0
filename = ''
startCity = 15
tourLength = 0
visited = []
rotate = False
flip = False

# The signal handler. On receiving sigterm, it writes
# the latest result to the file.
def sig_term(num, frame):
	global bestTour
	global bestLength
	global visited
	global tourLength
	
	if (bestLength < tourLength):
		visited = bestTour
	
	print "SIG-TERMINATED OUTPUT >>", tour_distance_check()
	output()

#function to calculate the Euclidean distance between two cities
def calc_dist(x1,y1,x2,y2):
	if ((x1 == x2) and (y1 == y2)):
		return 0
	else:
		#round to the nearest integer. 
		#For 0.1, put a one, then for 0.01 put 2, etc. negative values work in the other direction
		return round(math.sqrt((x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2)),0)

# function to output the visited tour file
def output():
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

	for cycle in range(30):
		#if (tour_size == cityCount):
		#	print "------------------------- CYCLE", cycle, "------------------------------"
		print "------------------------- CYCLE", cycle, "------------------------------"
		visited.reverse()
		for i in range(2, tour_size-1):
			if (i % 250 == 0):
				print "======= TOUR STOP", i, "of", tour_size-1, "========="
				tour_distance_check()
			for j in range(i, tour_size-1):
				opt_swap(visited[i-2], visited[i-1], visited[j], visited[j+1])

		#if (tour_size == cityCount):
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
	print 0, cityList[visited[0]][0], cityList[visited[0]][1]

	# distance from starting city to all other cities
	for x in range(1, len(visited)):
		thisDistance = calc_dist(cityList[visited[x-1]][0], cityList[visited[x-1]][1], cityList[visited[x]][0], cityList[visited[x]][1])
		cumDistance += thisDistance
		print x, cityList[visited[x]][0], cityList[visited[x]][1], "dist:", thisDistance, "cum dist:", cumDistance

	# distance back to first city
	thisDistance = calc_dist(cityList[visited[x]][0], cityList[visited[x]][1], cityList[visited[0]][0], cityList[visited[0]][1])
	cumDistance += thisDistance
	print 0, cityList[visited[0]][0], cityList[visited[0]][1], "dist:", thisDistance, "cum dist:", cumDistance

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
		#print "********** swapping [", A, B, "] and [", C, D,"] **********"
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

		#tour_distance_check()

# greedy tour
def get_greedy_tour():
	global visited
	global cityList
	global cityCount
	global startCity
	currCity = startCity
	thisDist = 0
	bestDist = 0
	bestCity = 0

	if (startCity >= cityCount):
		startCity = 0

	notVisited = []
	for i in range(cityCount):
		notVisited += [i]		
	visited = []

	# initiate the tour with first city
	notVisited.remove(startCity)
	visited.append(startCity)

	while (len(visited) < cityCount):

		# find next city to add
		bestDist = 999999999
		for i in range(len(notVisited)):
			x1 = cityList[currCity][0]
			y1 = cityList[currCity][1]
			x2 = cityList[notVisited[i]][0]
			y2 = cityList[notVisited[i]][1]
			thisDist = calc_dist(x1,y1,x2,y2)
			if (thisDist < bestDist):
				bestDist = thisDist
				bestCity = notVisited[i]

		notVisited.remove(bestCity)
		visited.append(bestCity)
		currCity = bestCity

	print "Initial GREEDY TOUR:", tour_distance_check()

# procedure to parse the input file, initialize the visited array, and optimize the tour
def find_tour():

# < Initializations > ------------------------------------------------

	global filename
	global cityList
	global cityCount
	global visited
	global tourLength
	global startCity
	global bestTour
	global bestLength
	global flip
	global rotate
	distance = 0
	tourCity = 0
	bestInterval = 0

	# variables to characterize city coordinate ranges
	x_max = 0
	y_max = 0
	x_min = 100000000
	y_min = 100000000
	x_step = 0
	y_step = 0
	x_idx = 0
	y_idx = 0
	intervals = 0	# chessboard squares per side of (intervals x intervals) chessboard

	# initialize cityList array
	with open(filename) as f:
		for line in f:
			cityList.append(map(int, line.strip().split()[1:3]))

	# get the count of cities
	cityCount = len(cityList)
	
# < Run time section > ------------------------------------------------

	# adjust starting interval number (default = 100) and define multi-run loop parameters
	intervals_first = 100
	intervals_last = 102
	if (cityCount < 100):
		intervals_first = 2
		intervals_last = 82
	elif (cityCount < 300):
		intervals_first = 2
		intervals_last = 52
	elif (cityCount < 1000):
		intervals_first = 2
		intervals_last = 62
	elif (cityCount < 1500):
		intervals_first = 2
		intervals_last = 62
	elif (cityCount < 3000):
		intervals_first = 2
		intervals_last = 62

	# execute specified number of runs; cover range of chessboard dimensions, if applicable
	for intervals in range(intervals_first, intervals_last, 2):


		print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< CHESSBOARD", intervals, "x", intervals, ">>>>>>>>>>"

		# declare mini-arrays for cities located in each chessboard square 
		mini_vis = [[0 for x in xrange(intervals*intervals)] for x in xrange(intervals*intervals)]

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

		# define dimensions of chessboard squares
		x_step = (x_max - x_min)/intervals + 1
		y_step = (y_max - y_min)/intervals + 1
	
		for i in range(intervals):
			for j in range(intervals):
				mini_vis[i*intervals + j] = []

		for i in range(cityCount):
			x_idx = (cityList[i][0] - x_min) / x_step
			y_idx = (cityList[i][1] - y_min) / y_step
			mini_vis[x_idx*intervals + y_idx].append(i)

		# Apply Chessboard tour algorithm to determine the order of the tour as it hops mini-segments
		tour_order = []
		curr_idx = 0

		# 	step1: add left edge of chess board, from upper left down to lower left
		for i in range(intervals):
			tour_order += [i*intervals]

		#	step2: add bottom edge of chess board, from left to right including lower right corner
		curr_idx = intervals * (intervals-1)
		for i in range(intervals-1):
			curr_idx += 1
			tour_order += [curr_idx]

		curr_idx -= intervals

		#	step3: add right edge of chess board, from bottom to top including top right corner
		tour_order += [curr_idx]
		for i in range(intervals-2):
			curr_idx -= intervals
			tour_order += [curr_idx]

		#	step4: while not adjacent to left edge, come in 2 columns at a time moving left
		#		add one column moving down from top; add one column moving up from bottom

		for loop in range(intervals/2 - 1):
			curr_idx -= 1
			tour_order += [curr_idx]
			for i in range(intervals-2):
				curr_idx += intervals
				tour_order += [curr_idx]

			curr_idx -= 1
			tour_order += [curr_idx]
			for i in range(intervals-2):
				curr_idx -= intervals
				tour_order += [curr_idx]
		
		orig_tour_order = tour_order

		# tour_order completed - optional output:
		#print tour_order

		"""
		#------example tour order on 10x10 chessboard (VISUAL REFERENCE ONLY)---------
		# defines the order city arrays per square are combined for the initial tour
		tour_order = [0,10,20,30,40,50,60,70,80,90]	<-- left edge of chessboard
		tour_order = [91,92,93,94,95,96,97,98,99]	<-- bottom edge of chessboard
		tour_order += [89,79,69,59,49,39,29,19,9]	<-- right edge of chessboard
		tour_order += [8,18,28,38,48,58,68,78,88]	<-- down a column to the left
		tour_order += [87,77,67,57,47,37,27,17,7]	<-- up a column to the left
		tour_order += [6,16,26,36,46,56,66,76,86]	<-- down a column to the left
		tour_order += [85,75,65,55,45,35,25,15,5]	<-- up a column to the left
		tour_order += [4,14,24,34,44,54,64,74,84]
		tour_order += [83,73,63,53,43,33,23,13,3]
		tour_order += [2,12,22,32,42,52,62,72,82]
		tour_order += [81,71,61,51,41,31,21,11,1]
		"""

		# form the initial tour by stringing the chessboard squares together
		visited = []
		for i in range(len(tour_order)):
			visited += mini_vis[tour_order[i]]

		# output initial tour number of cities and tour length
		tour_distance_check()
		#print visited		#optional output

		# optimize tour length by cycling through a number of 2-opt swaps and array reversals
		optimize_tour()
		tour_distance_check()
		#tour_distance_check_detail()	#optional output

		# record the current best tour
		if (tourLength < bestLength):
			bestLength = tourLength
			bestTour = visited
			bestInterval = intervals

		print "(BEST SO FAR:", bestLength, "FROM INTERVAL:", bestInterval,")"

		# ----------- run with flips -------------------
		if (flip):
			for flipnum in range(3):
				print "				|********** FLIP **********|"
				temp_tour = [0 for x in xrange(intervals*intervals)]
				tour_order = orig_tour_order
				for i in range(intervals):
					for j in range(intervals):
						# flip#1: flip tour_order horizontally
						if (flipnum==0):
							temp_tour[i*intervals + j] = tour_order[i*intervals + (intervals-j-1)] 
						# flip#2: flip tour_order vertically
						elif (flipnum==1):
							temp_tour[i*intervals + j] = tour_order[(intervals-i-1)*intervals + j] 
						# flip#3: flip tour_order diagnally
						else:
							temp_tour[i*intervals + j] = tour_order[i + j*intervals] 
				tour_order = temp_tour

				# form the initial tour by stringing the chessboard squares together
				visited = []
				for i in range(len(tour_order)):
					visited += mini_vis[tour_order[i]]

				# output initial tour number of cities and tour length
				tour_distance_check()
				#print visited		#optional output

				# optimize tour length by cycling through a number of 2-opt swaps and array reversals
				optimize_tour()
				tour_distance_check()
				#tour_distance_check_detail()	#optional output

				# record the current best tour
				if (tourLength < bestLength):
					bestLength = tourLength
					bestTour = visited
					bestInterval = intervals
		
				print "(BEST SO FAR:", bestLength, "FROM INTERVAL:", bestInterval, ")"

		# ----------- run with rotations -------------------
		if (rotate):
			for rotatenum in range(3):
				print "				|********** ROTATE **********|"
				temp_tour = [0 for x in xrange(intervals*intervals)]
				tour_order = orig_tour_order
				for i in range(intervals):
					for j in range(intervals):
						# rotate#1: clockwise one turn
						if (rotatenum==0):
							temp_tour[i*intervals + j] = tour_order[(intervals-i-1) + j*intervals] 
						# rotate#2: counterclockwise one turn
						elif (rotatenum==1):
							temp_tour[i*intervals + j] = tour_order[i + (intervals-j-1)*intervals] 
						# rotate#3: clockwise two turns
						else:
							temp_tour[i*intervals + j] = tour_order[(intervals-i-1)*intervals + (intervals-j-1)] 
				tour_order = temp_tour

				# form the initial tour by stringing the chessboard squares together
				visited = []
				for i in range(len(tour_order)):
					visited += mini_vis[tour_order[i]]

				# output initial tour number of cities and tour length
				tour_distance_check()
				#print visited		#optional output

				# optimize tour length by cycling through a number of 2-opt swaps and array reversals
				optimize_tour()
				tour_distance_check()
				#tour_distance_check_detail()	#optional output

				# record the current best tour
				if (tourLength < bestLength):
					bestLength = tourLength
					bestTour = visited
					bestInterval = intervals
		
				print "(BEST SO FAR:", bestLength, "FROM INTERVAL:", bestInterval, ")"

		"""
		# ----------- run with greedy algorithm -------------------
		for i in range(cityCount):
			startCity = i
			get_greedy_tour()
			# optimize tour length by cycling through a number of 2-opt swaps and array reversals
			optimize_tour()
			print "startCity", i, tour_distance_check()

			# record the current best tour
			if (tourLength < bestLength):
				bestLength = tourLength
				bestTour = visited
		"""

# < OUTPUT RESULTS > ------------------------------------------------
	visited = bestTour
	
	print "\nFINAL RESULT: from BEST INTERVAL", bestInterval	
	tour_distance_check()
	

	# write output to file
	output()

def main(argv):
	global filename
	global rotate
	global flip	

	# Register signal handler
	signal.signal(signal.SIGTERM, sig_term)
	
	opts, args = getopt.getopt(argv, "hf:RF", ["filename="])	
	
	for o, a in opts:
		if o == '-h':
			print 'usage: tsp.py -f <filename>'
			sys.exit()
		elif o in ("-f", "--filename"):
			filename = a
		elif o == '-R':
			rotate = True
		elif o == '-F':
			flip = True
		else:
			assert False, "unhandled option"	

	find_tour()

if __name__ == '__main__':
	main(sys.argv[1:])
