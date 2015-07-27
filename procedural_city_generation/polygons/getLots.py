from __future__ import division
from Polygon import Edge, Polygon
from getBlock import getBlock

def divide(poly):
	"""Divide polygon as many smaller polygons as possible"""
	current = [poly]
	nxt = []
	done = []
	while current:
		for x in current:
			split = x.split()
			if split:
				nxt += split
			else:
				done.append(x)
		current, nxt = nxt, []
	return done
	
def main(wedge_poly_list, vertex_list):
	properties = []
	for wedge_poly in wedge_poly_list:
		for poly in getBlock(wedge_poly, vertex_list):
			if poly.poly_type=="block":
				properties += divide(poly)
			else:
				properties.append(poly)
	return properties
	

	
	
if __name__=="__main__":
	import matplotlib.pyplot as plt
	import numpy as np
	import poly_plot as pp
	from getBlock import getBlock
	
	import construct_polygons as cp
	polys, vertices = cp.main()
	
	lots = main(polys[:30], vertices)
	print "%s lots found" %(len(lots))
	for p in lots:
		pp.plot_poly(p)
		
		
		
	plt.show()
