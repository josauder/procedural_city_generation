import numpy as np



def main(vertex_list=None,plotbool=False):
	'''Input: list of vertices representing the Roadmap
	Output: List of all Polygons representing Lots,
	List of all Polygons representing Blocks
	List of all Polygons which are too large to be Lots
	Polygon representing the road-network'''
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
	
	print "Extracting Polygons"
	from procedural_city_generation.polygons import construct_polygons
	polylist=construct_polygons.getPolygons(vertex_list)	
	print "Polygons extracted"
	
	
	
	
	#TODO: DISCUSS
	from procedural_city_generation.polygons.getLots import main as lennysmain
	"%s vertices" %(len(vertex_list))
	polygons=lennysmain(polylist[:2],vertex_list)
	
	print "Grundstuecke found"
	if plotbool:
		import matplotlib.pyplot as plt
		from poly_plot import plot_edge, plot_poly
		for g in polygons:
			plot_poly(g)
		plt.show()
		
		
	return 0

if __name__ == '__main__':
	main(None,True)


