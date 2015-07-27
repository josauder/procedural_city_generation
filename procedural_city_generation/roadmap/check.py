# -*- coding: utf-8 -*-
from __future__ import division
from Vertex import Vertex

import numpy as np
from config import Global_Lists, Variables
Global_Lists = Global_Lists()
variables = Variables()
from scipy.spatial import cKDTree


def sinnvoll(suggested_vertex,neighbour):
	#Checks if Nachbar is in Bounds
	if (abs(suggested_vertex.coords[0])>variables.border[0]-variables.maxLength) or (abs(suggested_vertex.coords[1])>variables.border[1]-variables.maxLength):
		return False
	
	#Finds all nearby Vertex and their distances
	distances,nearvertex=Global_Lists.tree.query(suggested_vertex.coords,10,distance_upper_bound=variables.maxLength)
	l=len(Global_Lists.vertex_list)
	nearvertex=[Global_Lists.vertex_list[x] for x in nearvertex if x<l ]
	
	#Distances[0] is the nearest Vertex:
	if distances[0]<variables.mindestabstand:
		
		if nearvertex[0] not in neighbour.neighbours:
			
			bestsol=np.inf
			solvertex=None
			
			for k in nearvertex:
				for n in k.neighbours:
					if n in nearvertex: #and not in doneliste
						sol=get_intersection(neighbour.coords,nearvertex[0].coords-neighbour.coords,k.coords,n.coords-k.coords)
						if sol[0]>0.00001 and sol[0]<0.99999 and sol[1]>0.00001 and sol[1]<0.99999 and sol[0]<bestsol:
							bestsol=sol[0]
							solvertex=[n,k]
	
			if solvertex is not None:
				solvertex[1].neighbours.remove(solvertex[0])
				solvertex[0].neighbours.remove(solvertex[1])
				newk=Vertex(neighbour.coords+bestsol*(nearvertex[0].coords-neighbour.coords))
				Global_Lists.vertex_list.append(newk)
				Global_Lists.coordsliste.append(newk.coords)
				Global_Lists.tree=cKDTree(Global_Lists.coordsliste,leafsize=160)
				neighbour.connection(newk)
				solvertex[1].connection(newk)
				solvertex[0].connection(newk)
				return False			
			else:
				nearvertex[0].connection(neighbour)
		return False
	bestsol=np.inf
	solvertex=None
	
	for k in nearvertex:
		for n in k.neighbours:
			if n in nearvertex: #and not in doneliste
				sol=get_intersection(neighbour.coords,suggested_vertex.coords-neighbour.coords,k.coords,n.coords-k.coords)
				if sol[0]>0.00001 and sol[0]<1.499999 and sol[1]>0.00001 and sol[1]<0.99999 and sol[0]<bestsol:
					bestsol=sol[0]
					solvertex=[n,k]
	if solvertex is not None:
		solvertex[1].neighbours.remove(solvertex[0])
		solvertex[0].neighbours.remove(solvertex[1])

		newk=Vertex(neighbour.coords+bestsol*(suggested_vertex.coords-neighbour.coords))
		Global_Lists.vertex_list.append(newk)
		Global_Lists.coordsliste.append(newk.coords)
		Global_Lists.tree=cKDTree(Global_Lists.coordsliste,leafsize=160)
		neighbour.connection(newk)
		solvertex[1].connection(newk)
		solvertex[0].connection(newk)
		return False
	return True

	
def get_intersection(a,ab,c,cd):
#					M=np.array([w1.v, -w2.v]).T
#					p2=v2.k1.coords
#					p1=neighbour.coords
#					loesung=np.linalg.solve(M, w2.p1-w1.p1)
	try:
		return np.linalg.solve(np.array([ab,-cd]).T,c-a)
	except np.linalg.linalg.LinAlgError:
		return np.array([np.inf,np.inf])
	
def check(suggested_vertex, neighbour, neufront):

	if sinnvoll(suggested_vertex , neighbour):
		#w=Weg(suggested_vertex,vertex) 
		suggested_vertex.connection(neighbour)
		neufront.append(suggested_vertex)
		Global_Lists.vertex_list.append(suggested_vertex)
		Global_Lists.coordsliste.append(suggested_vertex.coords)
		Global_Lists.tree=cKDTree(Global_Lists.coordsliste,leafsize=160)
#		Global_Lists.wegliste.append(w) 
	return neufront
