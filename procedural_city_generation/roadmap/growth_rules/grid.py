from __future__ import division
import numpy as np
import random
from procedural_city_generation.roadmap.Vertex import Vertex
from procedural_city_generation.additional_stuff.rotate import rotate
from procedural_city_generation.additional_stuff.Singleton import Singleton


singleton=Singleton("roadmap")

def grid(vertex,b):
	
	#Sammelt Numerische Werte aus Variables-Objekt
	pForward=singleton.gridpForward
	pTurn=singleton.gridpTurn
	lMin=singleton.gridlMin
	lMax=singleton.gridlMax
	
	
	suggested_vertices=[]	
	weiter=True
	
	
	#Berechnet den Vektor des letzten Weges zu diesem Punkt
	
	previous_vector=np.array(vertex.coords-vertex.neighbours[len(vertex.neighbours)-1].coords)
	previous_vector=previous_vector/np.linalg.norm(previous_vector)
	
	n=np.array([-previous_vector[1],previous_vector[0]])
	
	#Geradeaus
	v=random.uniform(lMin,lMax)*previous_vector
	random_number=random.randint(0,100)
	if random_number<=pForward:
		k=Vertex(vertex.coords+v)
		
		suggested_vertices.append(k)
		weiter=False
	#Rechts
	v=random.uniform(lMin,lMax)*previous_vector
	random_number=random.randint(0,100)
	if random_number<=pTurn*b*b:
		k=Vertex(vertex.coords+n)
		
		suggested_vertices.append(k)
		weiter=True
	
	#Links
	v=random.uniform(lMin,lMax)*previous_vector
	random_number=random.randint(0,100)
	if random_number<=pTurn*b*b:
		k=Vertex(vertex.coords-n)
		
		suggested_vertices.append(k)
		weiter=True
	
	
	#Seed!
	if not weiter:
		vertex.seed=True
		singleton.global_lists.vertex_queue.append([vertex, 0])
	
	return suggested_vertices

