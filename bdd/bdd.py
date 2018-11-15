######## BDD Programming Assignment ########

from pyeda.inter import *
from functools import reduce

def create_var(num):
	"""
		Converts a number into an array of boolean values
	"""
	return [(num & 1 << n) for n in range(4, -1, -1)]


def var_expression(name, arr):
	"""
		Creates an expression out of a boolean array
	"""
	_vars = bddvars(name, 5)
	_vars = [var if n else ~var for var, n in zip(_vars, arr)]
	return reduce(lambda m, n: m & n, _vars)
	

def create_bool_formula(i, j):
	""" 
		Creates a boolean formula based on the binary representation
		of the numbers given
	"""
	ex1 = var_expression('x', create_var(i))
	ex2 = var_expression('y', create_var(j))
	return ex1 & ex2


def init_bdd():
	""" 
		Creates the initial BDD for the project 
	"""
	n = 0
	for i in range(0, 32):
		for j in range(0, 32):
			if (i + 3) % 32 == j % 32 or (i + 7) % 32 == j % 32:
				if n != 0:
					f = create_bool_formula(i, j) | f
				else: 
					f = create_bool_formula(i, j)
					n = 1
	return expr2bdd(f)


def compose(r1, r2):
	"""
		Takes two graphs, and returns the composition of them
	"""
	x = bddvars('x', 5)
	y = bddvars('y', 5)
	z = bddvars('z', 5)
	for i in range(0, 4):
		r1 = r1.compose({x[i]: z[i]})
		r2 = r2.compose({y[i]: z[i]})
	r = r1 & r2
	return r.smoothing(z)


def create_fstar(g):
	"""
		Takes in a graph, and generates the transitive closure of it
	"""
	fstar = g
	while True:
		f = fstar
		fstar = f | compose(g, f)
		if fstar.equivalent(f):
			return fstar


# Main Program:

g = init_bdd()

fstar = create_fstar(g)

x = bddvars('x', 5)
y = bddvars('y', 5)

result = fstar.smoothing(x).smoothing(y).equivalent(True)

if(result):
	print("All nodes are reachable by all other nodes in G")
else:
	print("Not all nodes are reachable by all other nodes in G")



