"""
Created on 2015.08.17
@author: Jonathan Sauder - jsauder@campus.tu-berlin.de
"""

from __future__ import division
import random
import numpy as np
from copy import copy
import procedural_city_generation
from procedural_city_generation.building_generation.Polygon3D import Polygon3D
from procedural_city_generation.building_generation.building_tools import *

def normal(arr):
	return np.array([-arr[1],arr[0],0])


def randomcut(walls,housebool):
	"""
	Chooses a Cut for the creation of the floorplan from all available cuts. 
	Every cut functions by adding/replacing values in the numpy array of
	the walls' vertices. There are two main cuts. 
	All other cuts are a combination of these two cuts.
	The elementary cuts are::
		Ccut
		------------        ----+   +----	
		               ==>      |   |		
		                        +---+		
		Lcut
		--------+           ----+		
		        |     ==>       |		
		        |               +---+	
		        |                   |	
		
	Parameters
	----------
	- walls : procedural_city_generation.building_generation.walls object
	- housebool : boolean 
		Value showing if a building is a house or not
	
	Returns
	----------
	- procedural_city_generation.building_generation.walls object	
	"""
	
	#TODO: Get numeric values in some sort of conf file
	
	n=random.randint(0,100)	
	a1=random.uniform(0,0.4)
	a2=random.uniform(0,0.4)
	s=random.randint(0,walls.l-1)
	
	if walls.l==4:
		#Most "advanced" cuts rely on the assumption that the walls object
		# used to have 4 sides
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
				elif n<95:
					return Hcut2(walls,a1,a2,s)
				else:
					return Ccut2(walls,a1,a2,s)
		return walls
	#Those that do not, will create random combinations through Lcut and Ccut
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
	
	
def Zcut(walls,dist1,dist2,side):
	"""
	Cuts a four-sided walls object as follows:
	:: 
	    +-----------+               +-------+
	    |           |               |       |
	    |           |   ==>     +---+       |
	    |           |           |       +---+
	    |           |           |       |
	    +-----------+           +-------+
	
	Parameters
	----------
	walls : procedural_city_generation.building_generation.walls object
	dist1 : float 
		Determines the length of one of the two vectors of the cut
	dist2 : float
		Determines the length of one of the two vectors of the cut
	side  : int
		The pair of sides of the building which will be cut
	
	Returns
	-------
	procedural_city_generation.building_generation.walls object
	"""
	side=(side%2)+2
	v2=(walls.vertices[side]-walls.vertices[side-1])*dist2
	v1=(walls.vertices[side-2]-walls.vertices[side-1])*dist1
	walls=Lcut(walls,dist1,dist2,side,v1,v2)
	walls=Lcut(walls,dist1,dist2,side-2,-v1,-v2)
	return walls




def Lcut(walls,dist1,dist2,side,v1=None,v2=None):
	"""
	Cuts a four-sided walls object as follows:
	::  
	    +-----------+           +-----------+
	    |           |           |           |
	    |           |   ==>     |           |
	    |           |           |       +---+
	    |           |           |       |
	    +-----------+           +-------+
	
	Parameters
	----------
	walls : procedural_city_generation.building_generation.walls object
	dist1 : float 
		Determines the length of one of the two vectors of the cut
	dist2 : float 
		Determines the length of one of the two vectors of the cut
	side  : int
		The pair of sides of the building which will be cut
	
	Returns
	-------
	procedural_city_generation.building_generation.walls object
	"""
	verts=walls.vertices
	v1=v1 if (v1 is not None) else (verts[side-2]-verts[side-1])*dist1
	v2=v2 if (v2 is not None) else (verts[side]-verts[side-1])*dist2
	verts=np.insert(verts,side,np.array([verts[side-1]+v1+v2,verts[side-1]+v2]),axis=0)
	verts[side-1]+=v1
	return Walls(verts,walls.l+2)
	
	
	
def Ccut(walls,dist1,dist2,side):
	"""
	Cuts a four-sided walls-object as follows:
	::
		+-----------+           +---+   +---+
		|           |           |   |   |   |
		|           |   ==>     |   +---+   |
		|           |           |           |
		|           |           |           |
		+-----------+           +-----------+
		
	Parameters
	----------
	walls : procedural_city_generation.building_generation.walls object
	dist1 : float 
		Determines the length of one of the two vectors of the cut
	dist2 : float 
		Determines the length of one of the two vectors of the cut
	side  : int
		The pair of sides of the building which will be cut
	
	Returns
	-------
	procedural_city_generation.building_generation.walls object
	"""
	if dist2<dist1:
		dist1,dist2=dist2,dist1
	a=walls.vertices[side]
	v=walls.vertices[side-1]-a
	n=normal(v)
	a1=a+dist2*v
	b1=a+(1-dist2)*v
	a2=a1+dist1*n
	b2=b1+dist1*n
	
	return Walls(np.insert(walls.vertices,side,np.array([b1,b2,a2,a1]),axis=0),walls.l+4)

	
def Tcut(walls,dist1,dist2,side):
	"""
	Cuts a four-sided walls object as follows:
	:: 
	    +-----------+               +---+
	    |           |               |   |
	    |           |   ==>     +---+   +---+
	    |           |           |           |
	    |           |           |           |
	    +-----------+           +-----------+
	
	Parameters
	----------
	walls : procedural_city_generation.building_generation.walls object
	dist1 : float 
		Determines the length of one of the two vectors of the cut
	dist2 : 
		float Determines the length of one of the two vectors of the cut
	side  : int
		The pair of sides of the building which will be cut
	
	Returns
	-------
	procedural_city_generation.building_generation.walls object
	"""
	side=(side%2)+2
	v2=(walls.vertices[side]-walls.vertices[side-1])
	v1=(walls.vertices[side-2]-walls.vertices[side-1])
	walls=Lcut(walls,dist1,dist2,side,v1*dist1,v2*dist2)
	walls=Lcut(walls,dist1,dist2,side-1,v2*dist2,-v1*dist1)
	return walls
	
def Ycut(walls,dist1,dist2,side):
	"""
	Cuts a four-sided walls object as follows:
	:: 
	    +-----------+               +---+
	    |           |               |   |
	    |           |   ==>     +---+   +---+
	    |           |           |           |
	    |           |           |   +---+   |
	    +-----------+           +---+   +---+
	
	Parameters
	----------
	walls : procedural_city_generation.building_generation.walls object
	dist1 : float 
		Determines the length of one of the two vectors of the cut
	dist2 : float 
		Determines the length of one of the two vectors of the cut
	side  : int
		The pair of sides of the building which will be cut
	
	Returns
	-------
	procedural_city_generation.building_generation.walls object
	"""
	walls=Tcut(walls,dist1/2,dist2/2,side)
	walls=Ccut(walls,dist1/2,dist2/2,side-3)
	return walls

def Hcut(walls,dist1,dist2,side):
	"""	
	Cuts a four-sided walls object as follows:
	:: 
	    +-----------+           +---+   +---+
	    |           |           |   |   |   |
	    |           |   ==>     |   +---+   |
	    |           |           |   +---+   |
	    |           |           |   |   |   |
	    +-----------+           +---+   +---+
	
	Parameters
	----------
	walls : procedural_city_generation.building_generation.walls object
	dist1 : float 
		Determines the length of one of the two vectors of the cut
	dist2 : float 
		Determines the length of one of the two vectors of the cut
	side  : int
		The pair of sides of the building which will be cut
	
	Returns
	-------
	procedural_city_generation.building_generation.walls object
	"""
	
	walls=Ccut(walls,dist1,dist2/2,side)
	walls=Ccut(walls,dist1,dist2/2,side-2)	
	return walls
	
def Ccut2(walls,dist1,dist2,side):
	""" 
	A (n=2) recursive Ccut
	"""
	walls=Ccut(walls,dist1,dist2/2,side)
	walls=Ccut(walls,dist1,dist2/2,side+4)
	walls=Ccut(walls,dist1,dist2/2,side)	
	return walls


def Hcut2(walls,dist1,dist2,side):
	""" 
	A (n=2) recursive Hcut
	"""

	side=side%2
	walls=Ccut(walls,dist1,dist2/2,side)
	walls=Ccut(walls,dist1,dist2/2,side+4)
	walls=Ccut(walls,dist1,dist2/2,side)
	walls=Ccut(walls,dist1,dist2/2,side+14)
	walls=Ccut(walls,dist1,dist2/2,side+18)
	walls=Ccut(walls,dist1,dist2/2,side+14)	
	return walls

def Xcut(walls,dist1,dist2,side):
	"""
	Cuts a four-sided walls object as follows:
	:: 
		+-----------+           +---+   +---+
		|           |           |   +---+   |
		|           |   ==>     +-+       +-+
		|           |           +-+       +-+
		|           |           |   +---+   |
		+-----------+           +---+   +---+
	
	Parameters
	----------
	walls : procedural_city_generation.building_generation.walls object
	dist1 : float 
		Determines the length of one of the two vectors of the cut
	dist2 : float 
		Determines the length of one of the two vectors of the cut
	side  : int
		The pair of sides of the building which will be cut
	
	Returns
	-------
	procedural_city_generation.building_generation.walls object
	"""
	walls=Ccut(walls,dist1,dist2/4,0)
	walls=Ccut(walls,dist1,dist2/4,5)	
	walls=Ccut(walls,dist1,dist2/4,10)
	walls=Ccut(walls,dist1,dist2/4,15)	
	return walls



