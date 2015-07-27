from __future__ import division
import numpy as np
import random

from procedural_city_generation.roadmap.Vertex import Vertex
from procedural_city_generation.additional_stuff.rotate import rotate

from procedural_city_generation.roadmap.config import Variables, Global_Lists
variables,Global_Lists=Variables(),Global_Lists()


def minor_road(vertex,b):
	
	#Sammelt Numerische Werte aus Variables-Objekt
	pForward=variables.minor_roadpForward
	pTurn=variables.minor_roadpTurn
	lMin=variables.minor_roadlMin
	lMax=variables.minor_roadlMax
	
	
	suggested_vertices=[]
	
	
	#Berechnet den Vektor des letzten Weges zu diesem Punkt
	
	previous_vector=np.array(vertex.coords-vertex.neighbours[len(vertex.neighbours)-1].coords)
	previous_vector=previous_vector/np.linalg.norm(previous_vector)
	n=np.array([-previous_vector[1],previous_vector[0]])
	#Geradeaus
	v=random.uniform(lMin,lMax)*previous_vector
	random_number=random.randint(0,100)
	if random_number<pForward*b:
		k=Vertex(vertex.coords+v)
		#k.neighbours.append(vertex)
		k.minor_road=True
		suggested_vertices.append(k)
	
	#Rechts
	v=random.uniform(lMin,lMax)*previous_vector
	random_number=random.randint(0,100)
	if random_number<pTurn*b:
		k=Vertex(vertex.coords+n)
		#k.neighbours.append(vertex)
		k.minor_road=True
		suggested_vertices.append(k)
		
	#Links
	v=random.uniform(lMin,lMax)*previous_vector
	random_number=random.randint(0,100)
	if random_number<pTurn*b:
		k=Vertex(vertex.coords-n)
		#k.neighbours.append(vertex)
		k.minor_road=True
		suggested_vertices.append(k)
		
	return suggested_vertices
