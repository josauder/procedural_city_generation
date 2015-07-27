from __future__ import division
import numpy as np
from Polygon import Edge, Polygon
import matplotlib.pyplot as plt
import poly_plot as pp

def p_in_poly(poly, point):
    x,y = point
    n = len(poly)
    inside = False

    p1x,p1y = poly[0][0]
    for i in range(n+1):
        p2x,p2y = poly[i % n][0]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

def getBlock(wedges, vertex_list, minor_factor=0.04, main_factor=0.08, max_vertices=15, max_area=10):
	'''Calculate block to be divided into lots, as well as street polygons'''
	old_vertices = [vertex_list[wedge.b] for wedge in wedges]
	old_poly = Polygon([v.coords for v in old_vertices])
	pp.plot_poly(old_poly)
	
	if len(old_poly.vertices) > max_vertices or old_poly.area() > max_area:
		print "Too large!"
		return [old_poly]
	new_vertices = []
	polylist = []
	
	for i in xrange(len(old_vertices)):
		
		#Calculate position of new vertex
		a,b,c = old_vertices[i-2], old_vertices[i-1], old_vertices[i]
		v1 = a.coords - b.coords
		v2 = c.coords - b.coords
		n1 = np.array((-v1[1],v1[0]))/np.linalg.norm(v1)
		n2 = np.array((v2[1],-v2[0]))/np.linalg.norm(v2)

		#Change lengths of normal vectors depending on whether each
		#edge is a minor road or a main road
		if b.minor_road or a.minor_road:
			n1 *= minor_factor
		else:
			n1 *= main_factor
		if b.minor_road or c.minor_road:
			n2 *= minor_factor
		else:
			n2 *= main_factor
		
		#Check if current vertex is dead end
		if not 0 - 0.001 < wedge.alpha < 0 + 0.001:
			#Not a dead end: move edges which share this vertex
			#inwards along their normal vectors, find intersection
			intersection = np.linalg.solve(np.array(((v1),(v2))).T,(b.coords+n2)-(b.coords+n1))
				
			new = b.coords + n1 + intersection[0]*v1
			plt.plot(new[0], new[1], 'ro')
			#Check if new vertex is in old polygon
			if p_in_poly(old_poly.edges, new):
				#Append new vertex to lot polygon
				new_vertices.append(new)
				#Append street polygon to polylist
				street_vertices = [a.coords, b.coords, new, a.coords + n1]
				polylist.append(Polygon(street_vertices, is_road=True,
					is_minor_road=a.minor_road or b.minor_road))
			else:
				#New vertex not in polygon, return old polygon as street polygon
				print "Error!" + str(new)
				old_poly.is_road = True
				return [old_poly]
		
		else:
			#Dead end: determine two new vertices by adding the two normals
			#to current vector, then check if these are in old polygon
			new1, new2 = b.coords + n1, b.coords + n2
			plt.plot(new1[0], new1[1], 'ro')
			plt.plot(new2[0], new2[1], 'ro')
			if p_in_poly(old_poly.edges, new1) and p_in_poly(old_poly.edges, new2):
				new_vertices += [new1, new2]
				polylist.append(Polygon([a.coords + n1, new1, new2, c.coords + n2], is_road=True,
				is_minor_road = a.minor_road or b.minor_road or c.minor_road))
			else:
				print "Error!"
				old_poly.is_road = True
				return [old_poly]
				
	#All new vertices are in old polygon: return block and street polygons			
	polylist.append(Polygon(new_vertices, is_block=True))
	return polylist
	
if __name__=="__main__":
	import construct_polygons as cp
	polys, vertices = cp.main()
	for p in getBlock(polys[1], vertices):
		pp.plot_poly(p)
	plt.show()
	
	
