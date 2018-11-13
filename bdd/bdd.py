######## BDD Programming Assignment ########

from pyeda.inter import *

def createBoolFormula(i, j):
	""" 
		Creates a boolean formula based on the binary representation
		of the numbers given
	"""
	s1 = s2 = ""
	for n in range(4, -1, -1):
		if (i & (1 << n)) == 0:
			s1 += "~"
		if (j & (1 << n)) == 0:
			s2 += "~"
		s1 += ("x[%d] & " % (4 - n))
		s2 += ("y[%d]" % (4 - n))
		if n > 0:
			s2 += " & "
	s1 += s2
	return expr(s1)


def initBDD():
	""" 
		Creates the initial BDD for the project 
	"""
	n = 0
	for i in range(0, 32):
		for j in range(0, 32):
			if (i + 3) % 32 == j % 32 or (i + 7) % 32 == j % 32:
				if n != 0:
					f = Or(createBoolFormula(i, j), f)
				else: 
					f = createBoolFormula(i, j)
					n = 1
	return expr2bdd(f)


# Main Program:

g = initBDD()
