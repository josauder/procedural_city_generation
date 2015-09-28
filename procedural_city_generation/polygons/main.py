import numpy as np
from procedural_city_generation.additional_stuff.Singleton import Singleton
singleton=Singleton("polygons")


def main(vertex_list=None):
	'''Input: list of vertices representing the Roadmap
	Output: List of all Polygon2Ds representing Lots,
	List of all Polygon2Ds representing Blocks
	List of all Polygon2Ds which are too large to be Lots
	Polygon2D representing the road-network'''

	if vertex_list is None:
		from procedural_city_generation.additional_stuff import jsontools
		
		vertex_list=jsontools.reconstruct()
		print "Reconstructing of data structure finished"
	
	import os
	import procedural_city_generation
	path=os.path.dirname(procedural_city_generation.__file__)
	
	with open(path+"/temp/border.txt","r") as f:
		border=f.read()
	border=[int(x) for x in border.split(" ") if x is not '']
	
	print "Extracting Polygon2Ds"
	from procedural_city_generation.polygons import construct_polygons
	polylist=construct_polygons.getPolygon2Ds(vertex_list)	
	

	
	
	print "Polygon2Ds extracted"
	
	
	
	
	#TODO: DISCUSS
	from procedural_city_generation.polygons.getLots import getLots as getLots
	"%s vertices" %(len(vertex_list))
	polygons=getLots(polylist,vertex_list)
	
	print "Lots found"
	
	if singleton.plotbool:
		print "Plotting..."
		import matplotlib.pyplot as plt
		for g in polygons:
			g.selfplot()
		plt.show()
		
	
	import pickle
	with open(os.path.dirname(procedural_city_generation.__file__)+"/outputs/polygons.txt", "w") as f:
		s = pickle.dumps(polygons)
		f.write(s)
	
	singleton.kill()
	return 0

if __name__ == '__main__':
	from parent_path import parent_path
	import sys
	sys.path.append(parent_path(depth=3))
	main(None)


