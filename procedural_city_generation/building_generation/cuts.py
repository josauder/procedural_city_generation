
from __future__ import division
import random
import numpy as np
from copy import copy
import procedural_city_generation
from procedural_city_generation.building_generation.Polygon3D import Polygon3D
from procedural_city_generation.building_generation.building_tools import *

def normale(arr):
	return np.array([-arr[1],arr[0],0])




def randomcut(walls):
	#TODO: Get numeric values in some sort of conf file
	n=random.randint(0,100)	
	a1=random.uniform(0,0.4)
	a2=random.uniform(0,0.4)
	s=random.randint(0,walls.l-1)
	return Lcut(walls,a1,a2,s)
	#TODO: Fix
#	s=random.randint(0,len(walls)-1)
	if len(walls)==4:
		if n>20:
			if n<35:
				return Ccut(walls,a1,a2,s)
			elif n<47:
				return Hcut(walls,a1,a2,s)
			elif n<56:
				return Xcut(walls,a1,a2,s)
#			elif n<68:
#				return Lcut(walls,a1,a2,s)
#			elif n<77:
#				return Tcut(walls,a1,a2,s)
#			elif n<82:
#				return KeineAhnungcut(walls,a1,a2,s)
#			elif n<87:
#				return KeineAhnung2cut(walls,a1,a2,s)
#			else:
#				return Ycut(walls,a1,a2,s)
	else:
		for i in range(len(walls)):
			if random.randint(0,100)>50:
				if n>40:
					walls= Ccut(walls,a1,a2,i)
	return walls
	



		
	
	
def Zcut(walls,abstand1,abstand2,side):
	'''Lcut from two opposing sides'''
	walls=copy(walls)
	wall1=walls[side-1]
	wall2=walls[side]
	
	a=wall2[0]
	v1=wall1[0]-a
	v2=wall2[1]-a
	walls[side-1]=[wall1[0] , a+v1*abstand1 , a+v2*abstand2+v1*abstand1]
	
	walls[side]=[a+v2*abstand2+v1*abstand1 , a+v2*abstand2 , wall2[1]]
	
	
	walls[side+1]=[wall2[1] , wall2[1]+v1*abstand1 , wall2[1]+v1*abstand1-v2*abstand2]
	
	walls[side+2]=[wall2[1]+v1*abstand1-v2*abstand2 , wall2[1]+v1-abstand2*v2 , wall1[0]]
	
	return walls


	
def KeineAhnung2cut(walls,abstand1,abstand2,side):
	'''Lcut from two opposing sides'''
	walls=copy(walls)
	wall1=walls[side-1]
	wall2=walls[side]
	
	a=wall2[0]
	v1=wall1[0]-a
	v2=wall2[1]-a
	walls[side-1]=[wall1[0] , a+v1*abstand1 , a+v2*abstand2+v1*abstand1]
	
	walls[side]=[a+v2*abstand2+v1*abstand1 , a+v2*abstand2 , wall2[1]]
	
	
	walls[side+1]=[wall2[1] , wall2[1]+v1*abstand1 , wall2[1]+v1*(1-abstand1)-v2*abstand2]
	
	
	
	walls[side+2]=[wall2[1]+v1*(1-abstand1)-v2*abstand2 , wall2[1]+v1-abstand2*v2 , wall1[0]]
	
	return walls
	

def Lcut(walls,abstand1,abstand2,side):
	'''Lcut from two opposing sides'''
	
	verts=walls.vertices
	v1=(verts[side-2]-verts[side-1])*abstand1
	v2=(verts[side]-verts[side-1])*abstand2
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
	
	walls=copy(walls)
	wall0=walls[-2]
	wall1=walls[-1]
	wall2=walls[0]
	
	a=wall2[0]
	v1=wall1[0]-a
	v2=wall2[1]-a
	
	walls[-2]=[wall0[0],wall0[0]-(1-abstand2)*v2,a+(abstand2)*v2+(1-abstand1)*v1,a+(1-abstand1)*v1]	
	walls[-1]=[a+(1-abstand1)*v1,a+abstand1*v1]	
	walls[0]=[a+abstand1*v1,a+v2*abstand2+v1*abstand1,a+v2*abstand2,wall2[1]]
	return walls
	
def Ycut(walls,abstand1,abstand2,side):
	'''Tcut from one side, C cut from the other'''
	walls=Tcut(walls,abstand1/2,abstand2/2,side)
	walls=Ccut(walls,abstand1/2,abstand2/2,side+1)
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

def Ocut(coords,dist):
	'''Innenhof'''
	return coords


