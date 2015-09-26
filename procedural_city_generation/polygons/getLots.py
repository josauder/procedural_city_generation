from __future__ import division
from procedural_city_generation.polygons.Polygon2D import Edge, Polygon2D
from getBlock import getBlock
from split_poly import split_poly

def divide(poly):
	"""Divide polygon as many smaller polygons as possible"""
	current = [poly]
	nxt = []
	done = []
	while current:
		for x in current:
			parts = split_poly(x)
			if parts:
				nxt += parts
			else:
				done.append(x)
		current, nxt = nxt, []
	return done
	
def getLots(wedge_poly_list, vertex_list):
	properties = []
	for wedge_poly in wedge_poly_list:
		for poly in getBlock(wedge_poly, vertex_list):
			if poly.poly_type=="lot":
				properties += divide(poly)
			else:
				properties.append(poly)
	return properties
	

	
	
if __name__=="__main__":
	import sys
	from parent_path import parent_path
	sys.path.append(parent_path(depth=3))
	import matplotlib.pyplot as plt
	import numpy as np
	from getBlock import getBlock
	from getFoundation import getFoundation
	
	import construct_polygons as cp
	polys, vertices = cp.main()
	
	lots = getLots(polys, vertices)
	print "%s lots found" %(len(lots))
	for p in lots:
		p.selfplot()
	plt.show()
