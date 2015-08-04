
from __future__ import division
import random
import numpy as np
from copy import copy
import procedural_city_generation
from procedural_city_generation.building_generation.Polygon3D import Polygon3D

def normale(arr):
	if arr.size==2:
		n= np.array([arr[1],-arr[0]])
		return n
	else:
		n=np.array([arr[1],-arr[0],0])
		return n



def randomcut(walls):
	#TODO: Get numeric values in some sort of conf file
	n=random.randint(0,100)	
	a1=random.uniform(0,0.4)
	a2=random.uniform(0,0.4)
	s=0
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
			elif n<68:
				return Lcut(walls,a1,a2,s)
			elif n<77:
				return Tcut(walls,a1,a2,s)
			elif n<82:
				return KeineAhnungcut(walls,a1,a2,s)
			elif n<87:
				return KeineAhnung2cut(walls,a1,a2,s)
			else:
				return Ycut(walls,a1,a2,s)
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
	

def KeineAhnungcut(walls,abstand1,abstand2,side):
	'''Lcut from two opposing sides'''
	walls=copy(walls)
	wall1=walls[side-1]
	wall2=walls[side]
	
	a=wall2[0]
	v1=wall1[0]-a
	v2=wall2[1]-a
	walls[side-1]=[wall1[0] , a+v1*abstand1 , a+v2*abstand2+v1*abstand1]
	
	walls[side]=[a+v2*abstand2+v1*abstand1 , a+v2*abstand2 , wall2[1]]
	walls[side+1]=[wall2[1],wall2[1]+v1*abstand1,wall2[1]+v1*abstand1-v2*abstand2]
	walls[side+2]=[wall2[1]+v1*abstand1-v2*abstand2,wall2[1]+v1-abstand2*v2,wall1[0]]
	
	return walls	
	
	
def Lcut(walls,abstand1,abstand2,side):
	'''Cuts rectangle into L shape'''
	walls=copy(walls)
	wall1=walls[side-1]
	wall2=walls[side]
	
	a=wall2[0]
	v1=wall1[0]-a
	v2=wall2[1]-a
	walls[side-1]=[wall1[0],a+v1*abstand1,a+v2*abstand2+v1*abstand1]
	walls[side]=[a+v2*abstand2+v1*abstand1,a+v2*abstand2,wall2[1]]
	
	
	return walls
	
def Ccut(walls,abstand1,abstand2,side):
	'''Ccut from one side'''
	wall=walls[side]
	
	if len(wall)==2:
		if abstand2<abstand1:
			abstand1,abstand2=abstand2,abstand1
		a=wall[0]
		v=wall[1]-a
		n=normale(v)
		a1=a+abstand2*v
		b1=a+(1-abstand2)*v
		a2=a1+abstand1*n
		b2=b1+abstand1*n
		
		walls[side]=[wall[0],a1,a2,b2,b1,wall[1]]
	
#	print "\n\n\n\n\n\n\n"
#	for wall in walls:
#		print [[round(x[0],2),round(x[1],2)] for x in wall]
	return walls
	
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
	walls=Ccut(walls,abstand1,abstand2/2,side+2)	
	return walls
	
def Xcut(walls,abstand1,abstand2,side):
	'''Hcut from 2 sides == Ccut from 4 sides'''
	walls=Ccut(walls,abstand1,abstand2/4,0)
	walls=Ccut(walls,abstand1,abstand2/4,1)	
	walls=Ccut(walls,abstand1,abstand2/4,2)
	walls=Ccut(walls,abstand1,abstand2/4,3)	

	return walls

def Ocut(coords,dist):
	'''Innenhof'''
	return coords


