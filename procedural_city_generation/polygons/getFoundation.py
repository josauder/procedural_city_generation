import numpy as np

def getFoundation(poly, grid_width=0.05, min_area=0.25, eps=10**-5):
	street_edges = sorted([edge for edge in poly.edges if edge.bordering_street],
							key=lambda x: -x.length)
	start_edge = street_edges[0]
					
	#Set up grid points
	nv = start_edge.dir_vector / start_edge.length
	grid_points = [start_edge.v1 + nv * ((start_edge.length % grid_width)*0.5)]
	
	for x in range(int(start_edge.length // grid_width)):
		grid_points.append(grid_points[-1] + nv * grid_width)
		
	#Calculate possible rectangles
					
	
		
		
		
	
	
