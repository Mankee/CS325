#
# Team RADZ
# 
# CS325-400
# Project #4

import sys, getopt ,math

cityList = []
filename = ''

def find_tour():
	global filename
	global cityList
	fin = open(filename, "r")
	char = ""
	str = ""
	cityPieces = []

	for word in fin.read().split(): #first we split into giant array of words
		cityPieces.append(word)

	fin.close() #close the file, we are done with it

	for x in range(0, len(cityPieces)-2, 3): #now we sort into a 2d array with id, x, y at each index
		cityList.append((int(cityPieces[x]), int(cityPieces[x+1]), int(cityPieces[x+2])))

	del cityPieces[:] #delete from start to finish on the cityPieces

	#######################Now we start to play with the distances here#################################

	cityDistance = math.sqrt(math.pow((cityList[0][1] - cityList[1][1]),2) +
					    	  math.pow((cityList[0][2] - cityList[1][2]),2))

	cityDistance = round(cityDistance, 0) #round to the nearest integer. For 0.1, put a one, then for 0.01 put 2, etc. negative values work in the other direction

	# write output to file
	filename = filename + '.tour' 
	
	fout = open(filename,'w')
	fout.write("%.0f\n" % cityDistance) 
	for city in cityList:
		fout.write("{0:} {1:} {2:}\n".format(city[0], city[1], city[2]))
	
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
