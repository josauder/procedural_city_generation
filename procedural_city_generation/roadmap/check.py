# -*- coding: utf-8 -*-
from __future__ import division
from Vertex import Vertex

import numpy as np
from config import Global_Lists, Variables
from scipy.spatial import cKDTree

try:
	#In try-except because sphinx fails to document otherwise
	Global_Lists = Global_Lists()
	variables = Variables()
except:
	pass

def check(suggested_vertex, neighbour, newfront):
	"""
	Performs the following checks on a suggestes vertex and the suggested
	connection between this vertex and his last neighbour:
	
	1) Is the vertex out of bounds
		If yes, dont add this Vertex
	2) Is the vertex too close to an existing vertex
		If yes, change the vector that is checked in 4 and 5 from 
		[neighbor-suggested_vertex] to [neighbor-closest_existing_point]
	3) Does the the vector intersect an existing connection (road)
		If yes, only create the connection up until that intersection.
		Add that intersection to the Global_lists and fix the neighbor
		attribute of the existing connection that was "intersected".
	4) Does the vector stop shortly before an existing connection
		If yes, extend the connection up until that intersection.
		Add that intersection to the Global_lists and fix the neighbor
		attribute of the existing connection that was "intersected".
	If none of the above, simply add this vertex to the global_lists 
	and the new front and return the newfront. This is the only place 
	aftert config, where Vertices get added to the Global Lists. Every Time
	A vertex is added, the cKDTree used to find the closest vertices has to
	be updated.
	
	Parameters
	----------
	suggested_vertex : Vertex object
	neighbour : Vertex object
	newfront : list<Vertex>
	
	Returns
	-------
	newfront : list<Vertex>
	"""
	#Checks if Neighborbar is in Bounds
	if (abs(suggested_vertex.coords[0])>variables.border[0]-variables.maxLength) or (abs(suggested_vertex.coords[1])>variables.border[1]-variables.maxLength):
		return newfront
	
	#Finds all nearby Vertex and their distances
	distances,nearvertex=Global_Lists.tree.query(suggested_vertex.coords,10,distance_upper_bound=variables.maxLength)
	l=len(Global_Lists.vertex_list)
	nearvertex=[Global_Lists.vertex_list[x] for x in nearvertex if x<l ]
	
	#Distances[0] is the distance to the nearest Vertex, nearve:
	if distances[0]<variables.mindestabstand:
		
		#If the nearest Vertex is not a neighbor
		if nearvertex[0] not in neighbour.neighbours:
			
			#Find the best solution - as in the closest intersection
			bestsol=np.inf
			solvertex=None
			
			for k in nearvertex:
				for n in k.neighbours:
					if n in nearvertex: #and not in doneliste
						sol=get_intersection(neighbour.coords,nearvertex[0].coords-neighbour.coords,k.coords,n.coords-k.coords)
						if sol[0]>0.00001 and sol[0]<0.99999 and sol[1]>0.00001 and sol[1]<0.99999 and sol[0]<bestsol:
							bestsol=sol[0]
							solvertex=[n,k]
			# If there is at least one solution, intersect that solution
			# See docstring #3 and #4
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
				return newfront
			else:
				#If there is no solution, the Vertex is clear
				#See docstring finish
				nearvertex[0].connection(neighbour)
		return newfront
		
	bestsol=np.inf
	solvertex=None
	
	#If there is not an existing vertex too close, do the same thing but with
	# The vector between the suggested vertex and its neighbro
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
		return newfront
	
	#If the Vertex is clear to go, add him and return newfront.
	
	suggested_vertex.connection(neighbour)
	neufront.append(suggested_vertex)
	Global_Lists.vertex_list.append(suggested_vertex)
	Global_Lists.coordsliste.append(suggested_vertex.coords)
	Global_Lists.tree=cKDTree(Global_Lists.coordsliste,leafsize=160)
	return newfront
	
def get_intersection(a,ab,c,cd):
	"""Gets the intersection coordinates between two lines.
	If it does not exist (lines are parrallel), returns np.array([np.inf,np.inf])
	
	Parameters
	----------
	a : np.ndarray(2,1)
		Starting point of first vector
	ab : np.ndarray(2,1)
		First vector (b-a)
	c : np.ndarray(2,1)
		Starting point of second vector
	cd : np.ndarray(2,1)
		Second vector (d-c)
		
	Returns
	-------
	intersection : np.ndarray(2,1)
	"""
	try:
		return np.linalg.solve(np.array([ab,-cd]).T,c-a)
	except np.linalg.linalg.LinAlgError:
		return np.array([np.inf,np.inf])
