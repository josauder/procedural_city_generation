from __future__ import division

import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt



class Wedge(object):
	def __init__(self,a,b,c,alpha):
		self.a=a
		self.b=b
		self.c=c
		self.alpha=alpha
	def __repr__(self):
		return "W["+str(self.a)+",\t"+str(self.b)+",\t"+str(self.c)+"]"

def getWedges(vertex_list):
	'''Constructs all inner Angles as Wedges of the Vertices A-B-C so that there exists exactly one Wedge B-C-X1.'''
	from operator import itemgetter,attrgetter
	allWedges=[]
	
	for vertex in vertex_list:
		orderedconnections=[]	
		number_of_neighbours=0
		for neighbour in vertex.neighbours:
			
			alpha=np.arctan2(neighbour.coords[1]-vertex.coords[1], neighbour.coords[0]-vertex.coords[0])
			if alpha<0:
				alpha+=2*np.pi
			orderedconnections.append([ neighbour.selfindex, alpha])
			number_of_neighbours+=1
		
		
		orderedconnections.sort(key=itemgetter(1))
		
		
		for i in range(number_of_neighbours):
			this=orderedconnections[i-1]
			afterthis=orderedconnections[i]
			if i == 0:
				winkel = this[1] - afterthis[1] + 2*np.pi
			else:
				winkel = afterthis[1]-this[1]
			winkel %= 2*np.pi
			neueswedge=Wedge(this[0],vertex.selfindex,afterthis[0],winkel)
			allWedges.append(neueswedge)
			
	allWedges.sort(key=attrgetter('a','b'))
	return allWedges



def getPolygons(vertex_list):
	'''Finds all closed Polygons. The algorithm starts with Wedge A-B-C and looks for Wedge B-C-X1, C-X1-X2... A polygon is found when Xn==A'''
	wedgeliste=getWedges(vertex_list)
	
	from bisect import bisect_left as search
	allpolygons=[]
	
	def search(x):
		s1=x.b
		s2=x.c
		for wedge in wedgeliste:
			if wedge.a==s1 and wedge.b==s2:
				return wedge
	
	while len(wedgeliste)>0:
		start=x=wedgeliste[0]
		currentpolygon=[]	
		while True:
			if not (np.pi - 0.001 < x.alpha < np.pi + 0.001) :
				currentpolygon.append(x)
			x=search(x)
			if x is not None:
				wedgeliste.remove(x)
				if x is start:
				
					allpolygons.append(currentpolygon)
					break
	return allpolygons


def main():
	from procedural_city_generation.additional_stuff import jsontools
	vertex_list=jsontools.reconstruct("output.json")
	print "Reconstruct finished, extracting Polygons"
	polylist=getPolygons(wedgeliste,vertex_list)	
	return polylist,vertex_list

if __name__ =='__main__':
	main()
		
		
		
		
		
		
