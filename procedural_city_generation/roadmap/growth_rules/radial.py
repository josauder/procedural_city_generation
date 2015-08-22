from __future__ import division
import numpy as np
import random
import math

from procedural_city_generation.roadmap.Vertex import Vertex
from procedural_city_generation.additional_stuff.rotate import rotate
from procedural_city_generation.roadmap.config import Variables, Global_Lists

try:
	#In try-except because sphinx fails to document otherwise
	Global_Lists = Global_Lists()
	variables = Variables()
except:
	pass

def radial(zentrum,vertex,b):

	
	#Sammelt Numerische Werte aus Variables-Objekt
	pForward=variables.radialpForward
	pTurn=variables.radialpTurn
	lMin=variables.radiallMin
	lMax=variables.radiallMax
	
	#Berechnet Radialvector und Vektor des letzten Weges zu diesem Punkt
	radialvector=vertex.coords-zentrum
	previous_vector=np.array(vertex.coords-vertex.neighbours[len(vertex.neighbours)-1].coords)
	previous_vector=previous_vector/np.linalg.norm(previous_vector)
	
	suggested_vertices=[]
	weiter=False
	
	#Berechnet, ob der Vektor eher Radial oder Tangential verlaeuft
	alpha=fallunterscheidung(previous_vector,radialvector)
	previous_vector=rotate(alpha,previous_vector)
	
	
	#Geradeaus
	v=random.uniform(lMin,lMax)*previous_vector
	random_number=random.randint(0,100)
	if random_number<=pForward:
		k=Vertex(vertex.coords+v)
		suggested_vertices.append(k)
	
	#Rechts
	v=random.uniform(lMin,lMax)*previous_vector
	random_number=random.randint(0,100)
	if random_number<=pTurn*b*b:
		k=Vertex(vertex.coords+rotate(90,v))
		suggested_vertices.append(k)
		weiter=True
	
	#Links
	v=random.uniform(lMin,lMax)*previous_vector
	random_number=random.randint(0,100)
	if random_number<=pTurn*b*b:
		k=Vertex(vertex.coords-rotate(90,v))
		suggested_vertices.append(k)
		weiter=True
	
	
	#Seed!
	if not weiter:
		vertex.seed=True
		Global_Lists.vertex_queue.append([vertex, 0])

	
	return suggested_vertices

def fallunterscheidung(v1,v2):
	'''Entscheided ob v1 eher Radial oder eher Tangential verlaeuft'''
	
	alpha1=math.atan2(v1[1],v1[0])
	alpha2=math.atan2(v2[1], v2[0])
	alpha= (alpha2-alpha1)*180/np.pi
	if alpha<0:
		alpha+=360
	if (alpha >=45 and alpha <90) or (alpha>=225 and alpha<270):
		alpha-=90
	elif (alpha >=90   and alpha <135  ) or (alpha>=270    and alpha < 315  ):
		alpha+=90
	
	elif (alpha>=135 and alpha <225):
		alpha-=180
	
	return alpha
