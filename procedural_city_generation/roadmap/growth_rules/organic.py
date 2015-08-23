from __future__ import division

import numpy as np
import random

from procedural_city_generation.roadmap.Vertex import Vertex
from procedural_city_generation.additional_stuff.rotate import rotate

from procedural_city_generation.additional_stuff.Singleton import Singleton

singleton=Singleton("roadmap")

def organic(vertex,b):
	
	#Sammelt Numerische Werte aus Variables-Objekt
	pForward=singleton.organicpForward
	pTurn=singleton.organicpTurn
	lMin=singleton.organiclMin
	lMax=singleton.organiclMax
	
	
	suggested_vertices=[]
	weiter=False
	
	#Berechnet den Vektor des letzten Weges zu diesem Punkt
	previous_vector=np.array(vertex.coords-vertex.neighbours[len(vertex.neighbours)-1].coords)
	previous_vector=previous_vector/np.linalg.norm(previous_vector)
	
	
	#Geradeaus
	v=random.uniform(lMin,lMax)*previous_vector
	random_number=random.randint(0,100)
	if random_number<=pForward:
		k=Vertex(vertex.coords+rotate(np.random.uniform(-30,30),v))
		suggested_vertices.append(k)
	
	#Rechts
	v=random.uniform(lMin,lMax)*previous_vector
	random_number=random.randint(0,100)
	if random_number<=b*pTurn:
		k=Vertex(vertex.coords+rotate(np.random.uniform(-120,-60),v))
		suggested_vertices.append(k)
		weiter=True
	
	#Links
	v=random.uniform(lMin,lMax)*previous_vector
	random_number=random.randint(0,100)
	if random_number<=b*pTurn:
		k=Vertex(vertex.coords+rotate(np.random.uniform(60,120),v))
		suggested_vertices.append(k)
		weiter=True
	
	#Seed!
	if not weiter:
		vertex.seed=True
		singleton.global_lists.vertex_queue.append([vertex, 0])
	
	return suggested_vertices
