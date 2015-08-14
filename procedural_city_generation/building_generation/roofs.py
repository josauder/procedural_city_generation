# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt

from procedural_city_generation.building_generation.cuts import *
from procedural_city_generation.building_generation.building_tools import *
from procedural_city_generation.building_generation.Polygon3D import Polygon3D
from procedural_city_generation.additional_stuff.Singleton import Singleton
singleton=Singleton("building_generation")

def roof(walls,roofwalls,currentheight,housebool,texture,texture2=None):
	"""Builds a roof on top of a house, depending on housetype
	Parameters
	----------
	TODO
	- walls  :  procedural_city_generation.building_generation.Walls object with cuts
	- roofwalls   :  procedural_city_generation.building_generation.Walls object without cuts
	- currentheight   :
	- housebool  :  
	- texture
	
	"""
	
	roofheight=np.random.uniform(singleton.roofheight_min,singleton.roofheight_max)

	if roofwalls.l==4 and housebool:
		return houseroof(roofwalls,currentheight, roofheight,texture)
	else:
		return kastenroof(walls,currentheight,texture,texture2)


def houseroof(walls, currentheight,roofheight, texture):
	"""Creates a "classic" roof with two triangles and two rectangles. 
	Used only for houses and assumes that the house has 4 sides.
	
	Parameters
	-----------
	- walls : procedural_city_generation.building_generation.Walls object
	- currentheight : height of the top of the building
	- roofheight : height of the roof itself
	- texture : procedural_city_generation.building_generation.Texture object
	
	Returns
	-----------
	- procedural_city_generation.building_generation.Polygon3D object
	
	"""
	#Differentiation: the shorter of the first two walls is to be cut in half
	if not np.linalg.norm(np.diff(walls.walls[0],axis=0))<np.linalg.norm(np.diff(walls.walls[1],axis=0)):
		walls=Walls(np.roll(walls.vertices,1,axis=0),walls.l)
	
	h_low=np.array([0,0,currentheight])
	h_high=h_low+np.array([0,0,roofheight])
	
	#The gable coordinates
	c1,c2=sum(walls.walls[0]/2),sum(walls.walls[2]/2)
	
	#Verts are the vertices of the wall and the vertices of the gable
	verts=[x+h_low for x in walls.vertices]+[c1+h_high,c2+h_high]
	
	#Faces are two rectangles and two triangles
	faces=[(0,1,5,4),(3,2,5,4),(0,3,4),(1,2,5)]
	return Polygon3D(verts,faces,texture)
	
	
def kastenroof(walls,currentheight,texture,texture2=None):
	#TODO
	return Polygon3D(walls.vertices+np.array([0,0,currentheight]),[range(walls.l)],texture)





def isleft(walls,point):
	return ((kante[1][0]-kante[0][0])*(point[1]-kante[0][1]) - (point[0]-kante[0][0]) * (kante[1][1]-kante[0][1]))
	
def p_in_poly(kanten,point):
	"""
	Returns True if a point is in a "walls" polygon
	
	Parameters
	----------
	- walls  :  procedural_city_generation.building_generation.walls object
	- point : np.ndarray with shape (3,)
	
	Returns
	----------
	- boolean : true if point in polygon, else false
	"""
	counter=0
	
	#TODO
	for wall in walls.walls:
		if kante[0][1] <= point[1]:
			if kante[1][1] > point[1]:
				if isleft(kante,point) >0:
					counter+=1
			elif kante[1][1] <= point[1]:
				if isleft(kante,point) <0:
					counter-=1
	if counter!=0:
		return True
	return False
