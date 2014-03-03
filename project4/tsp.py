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

import sys, getopt, math

cityList = []
cityCount = 0
visited = []
filename = ''
tourLength = 0
startCity = 15

#function to calculate the Euclidean distance between two cities
def calc_dist(x1,y1,x2,y2):
	if ((x1 == x2) and (y1 == y2)):
		return 0
	else:
		#round to the nearest integer. 
		#For 0.1, put a one, then for 0.01 put 2, etc. negative values work in the other direction
		return round(math.sqrt(math.pow((x1 - x2),2) + math.pow((y1 - y2),2)),0)

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

# basic routine to optimize tour length by cycling through a number of 2-opt swaps and array reversals
def optimize_tour():
	global visited

	visited.reverse()

	for cycle in range(10):
		#print "------------------------- CYCLE", cycle, "------------------------------"
		for i in range(2, cityCount-1):
			for j in range(i, cityCount-1):
				opt_swap(visited[i-2], visited[i-1], visited[j], visited[j+1])

	visited.reverse()

	for cycle in range(10):
		#print "------------------------- CYCLE", cycle, "------------------------------"
		for i in range(2, cityCount-1):
			for j in range(i, cityCount-1):
				opt_swap(visited[i-2], visited[i-1], visited[j], visited[j+1])


# calculates the tour length given the current visited[] array.  Outputs city count and tour length.
def tour_distance_check():
	global visited
	global tourLength

	thisDistance = 0
	cumDistance = 0

	# distance from starting city to all other cities
	for x in range(1, cityCount):
		thisDistance = calc_dist(cityList[visited[x-1]][0], cityList[visited[x-1]][1], cityList[visited[x]][0], cityList[visited[x]][1])
		cumDistance += thisDistance

	# distance back to first city
	thisDistance = calc_dist(cityList[visited[x]][0], cityList[visited[x]][1], cityList[visited[0]][0], cityList[visited[0]][1])
	cumDistance += thisDistance

	print "#cities:", cityCount, "Length:", cumDistance
	tourLength = cumDistance

# calculates the tour length given the current visited[] array.  Outputs city count and tour length.
# Additional output includes all cities, coordinates, and incremental/cumulative distances of the tour.
def tour_distance_check_detail():
	global visited
	global tourLength

	thisDistance = 0
	cumDistance = 0

	# check figures: cities and main program tourLength
	print "\n#cities:", cityCount, "Length:", tourLength

	# first city - this is the tour starting point
	print 0, cityList[visited[0]][0], cityList[visited[0]][1], cityList[visited[0]][2]

	# distance from starting city to all other cities
	for x in range(1, cityCount):
		thisDistance = calc_dist(cityList[visited[x-1]][1], cityList[visited[x-1]][2], cityList[visited[x]][1], cityList[visited[x]][2])
		cumDistance += thisDistance
		print x, cityList[visited[x]][0], cityList[visited[x]][1], cityList[visited[x]][2], "dist:", thisDistance, "cum dist:", cumDistance

	# distance back to first city
	thisDistance = calc_dist(cityList[visited[x]][1], cityList[visited[x]][2], cityList[visited[0]][1], cityList[visited[0]][2])
	cumDistance += thisDistance
	print 0, cityList[visited[0]][0], cityList[visited[0]][1], cityList[visited[0]][2], "dist:", thisDistance, "cum dist:", cumDistance

	print "#cities:", cityCount, "Length:", cumDistance
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
	fout = 0
	distance = 0
	tourCity = 0

	with open(filename) as f:
		for line in f:
			cityList.append(map(int, line.strip().split()[1:3]))

	#get the count of cities
	cityCount = len(cityList)

	#go on a tour {note: at this stage, starting city 15 is optimal for sample1; city 165 is optimal for sample2}
	if (startCity > cityCount):
		startCity = 0
	tourCity = startCity
	visited.append(tourCity)
	for c in range(cityCount - 1):
		tourCity = find_short_path(tourCity)
		visited.append(tourCity)

	#-----added by Rittie----------------------------------------------
	#for x in range(cityCount):
	#	print cityList[x][0], cityList[x][1], cityList[x][2]

	#tour_distance_check_detail()
	optimize_tour()
	tour_distance_check()
	#------------------------------------------------------------------

	# write output to file
	filename += '.tour' 

	fout = open(filename,'w')
	fout.write("%.0f\n" % tourLength)
	for city in visited:
		fout.write("{0}\n".format(city))
	
	fout.close()

def main(argv):
	global filename

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
