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
	
def main(wedge_poly_list, vertex_list, max_vertices=20, max_area=5):
	properties = []
	for wedge_poly in wedge_poly_list:
		for poly in getBlock(wedge_poly, vertex_list):
			if poly.is_block:
				properties += divide(poly)
			else:
				properties.append(poly)
	return properties
	

	
	
if __name__=="__main__":
	from poly_plot import *
	from getBlock import getBlock

	p = [np.array(x) for x in [[0,0],[0,2],[2,1.7],[1.8,0]]]
	poly = Polygon(p)
	
	fig = plt.figure()
	plt.pause(0.01)
	poly.selfplot()
	fig.canvas.draw()
	raw_input("> ")
	for new in divide(poly):
		print "New Polygon:"
		print new
		print "#"*20
		new.selfplot()
		fig.canvas.draw()
		raw_input("> ")
		
		
		
	plt.show()
