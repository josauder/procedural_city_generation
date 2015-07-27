from __future__ import division
import numpy as np
import math

def findsquare(poly):
	base= max([edge for edge in poly.edges if edge.bordering_road], key=lambda edge:edge.length)
	point1=base.vertex1
	intersections=[], volume=0, n=2
	while n=2:
		point1+=base.normal/global.findsquareinpoly.aufloesung
		newintersections=[]
		for edge in [edge in poly.edges if edge is not base]:
			try L=np.linalg.solve(np.array([base.dir_vector, -edge.dir_vector]).T, point1-edge.vertex1):
				if 0<L[0]<1 and 0<L[1]<1 :
					newintersections.append(base.dir_vector*L[0]+point1)
			except: pass
		n=len(newintersections)
		newvolume= abs(point1-base.vertex1)*abs(newintersections[1]-newintersections[0])
		if newvolume>volume:
			intersections=newintersections, volume=newvolume

	return intersections
