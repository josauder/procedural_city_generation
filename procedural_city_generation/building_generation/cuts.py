
from __future__ import division
import random
import numpy as np
from copy import copy
import procedural_city_generation
from procedural_city_generation.building_generation.Polygon3D import Polygon3D
from procedural_city_generation.building_generation.building_tools import *

def normale(arr):
	return np.array([-arr[1],arr[0],0])




def randomcut(walls,housebool):
	#TODO: Get numeric values in some sort of conf file
	n=random.randint(0,100)	
	a1=random.uniform(0,0.4)
	a2=random.uniform(0,0.4)
	s=random.randint(0,walls.l-1)
	
	if walls.l==4:
		if (not housebool) or (random.uniform(0,1)<0.5):
			if n>20:
				if n<35:
					return Ccut(walls,a1,a2,s)
				elif n<47:
					return Hcut(walls,a1,a2,s)
				elif n<56:
					return Xcut(walls,a1,a2,s)
				elif n<68:
					return Lcut(walls,a1,a2,s)
				elif n<77:
					return Tcut(walls,a1,a2,s)
				elif n<87:
					return Ycut(walls,a1,a2,s)
		return walls
	else:
		k=0
		for i in range(walls.l):
			if random.randint(0,100)>50:
				if n>40:
					walls= Ccut(walls,a1,a2,i+k)
					k+=4
				elif n>45:
					walls=Lcut(walls,a1,a2,i+k)
					k+=2
	return walls
	



		
	
	
def Zcut(walls,abstand1,abstand2,side):
	'''Lcut from two opposing sides'''
	side=(side%2)+2
	v2=(walls.vertices[side]-walls.vertices[side-1])*abstand2
	v1=(walls.vertices[side-2]-walls.vertices[side-1])*abstand1
	walls=Lcut(walls,abstand1,abstand2,side,v1,v2)
	walls=Lcut(walls,abstand1,abstand2,side-2,-v1,-v2)
	return walls




def Lcut(walls,abstand1,abstand2,side,v1=None,v2=None):
	'''Lcut from two opposing sides'''
	verts=walls.vertices
	v1=v1 if (v1 is not None) else (verts[side-2]-verts[side-1])*abstand1
	v2=v2 if (v2 is not None) else (verts[side]-verts[side-1])*abstand2
	
	verts=np.insert(verts,side,np.array([verts[side-1]+v1+v2,verts[side-1]+v2]),axis=0)
	verts[side-1]+=v1
	return Walls(verts,walls.l+2)
	
	
	
def Ccut(walls,abstand1,abstand2,side):
	'''Ccut from one side'''
	if abstand2<abstand1:
		abstand1,abstand2=abstand2,abstand1
	a=walls.vertices[side]
	v=walls.vertices[side-1]-a
	n=normale(v)
	a1=a+abstand2*v
	b1=a+(1-abstand2)*v
	a2=a1+abstand1*n
	b2=b1+abstand1*n
	
	return Walls(np.insert(walls.vertices,side,np.array([b1,b2,a2,a1]),axis=0),walls.l+4)

	
def Tcut(walls,abstand1,abstand2,side):
	'''Lcut from two sides'''
	side=(side%2)+2
	v2=(walls.vertices[side]-walls.vertices[side-1])
	v1=(walls.vertices[side-2]-walls.vertices[side-1])
	walls=Lcut(walls,abstand1,abstand2,side,v1*abstand1,v2*abstand2)
	walls=Lcut(walls,abstand1,abstand2,side-1,v2*abstand2,-v1*abstand1)
	return walls
	
def Ycut(walls,abstand1,abstand2,side):
	'''Tcut from one side, C cut from the other'''
	walls=Tcut(walls,abstand1/2,abstand2/2,side)
	walls=Ccut(walls,abstand1/2,abstand2/2,side-3)
	return walls

def Hcut(walls,abstand1,abstand2,side):
	'''Ccut from both sides'''

	walls=Ccut(walls,abstand1,abstand2/2,side)
	walls=Ccut(walls,abstand1,abstand2/2,side-2)	
	return walls
	
def Ccut2(walls,abstand1,abstand2,side):
	'''Ccut from one side sides and ccut on each of those sides'''
	walls=Ccut(walls,abstand1,abstand2/2,side)
	walls=Ccut(walls,abstand1,abstand2/2,side+4)
	walls=Ccut(walls,abstand1,abstand2/2,side)	
	return walls


def Hcut2(walls,abstand1,abstand2,side):
	
	'''Ccut from one side sides and ccut on each of those sides'''
	side=side%2
	walls=Ccut(walls,abstand1,abstand2/2,side)
	walls=Ccut(walls,abstand1,abstand2/2,side+4)
	walls=Ccut(walls,abstand1,abstand2/2,side)
	walls=Ccut(walls,abstand1,abstand2/2,side+14)
	walls=Ccut(walls,abstand1,abstand2/2,side+18)
	walls=Ccut(walls,abstand1,abstand2/2,side+14)	
	return walls

def Xcut(walls,abstand1,abstand2,side):
	'''Hcut from 2 sides == Ccut from 4 sides'''
	walls=Ccut(walls,abstand1,abstand2/4,0)
	walls=Ccut(walls,abstand1,abstand2/4,5)	
	walls=Ccut(walls,abstand1,abstand2/4,10)
	walls=Ccut(walls,abstand1,abstand2/4,15)	
	return walls



