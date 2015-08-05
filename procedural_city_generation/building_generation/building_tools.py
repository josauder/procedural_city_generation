from __future__ import division
import random
import numpy as np
from copy import copy
import procedural_city_generation
from procedural_city_generation.building_generation.Polygon3D import Polygon3D

def walls_from_poly(poly):
	"""Creates a wall object from a Polygon3D Object by converting 
	Poly.vertices from 2D-Arrays to 3D, np.array([x,y])->np.array([x,y,0])
	
	Parameters
	----------
	- poly : procedural_city_generation.building_generation.Polygon3D object
	
	Returns
	----------
	- procedural_city_generation.building_generation.Walls object
	
	"""
	l=len(poly.vertices)
	return Walls(np.hstack((np.array(poly.vertices),[[0]]*l)),l)


class Walls(object):
		
	def __init__(self,verts,l):
		self.vertices=verts
		self.l=l
		
		self.center=sum(self.originalcenter)/self.l
		self.walls=np.array([self.originalvertices[[i,i-1]] for i in range(self.l)])
		


def scale(walls,factor):
	"""Scales a walls object by a factor
	Parameters
	----------
	- walls  :  procedural_city_generation.building_generation.Walls object
	- factor :  number to be scaled to. E.g. 2 doubles the size, 0.5 halves the size
	
	Returns
	----------
	- procedural_city_generation.building_generation.Walls object
	"""
	return Walls(walls.center+(walls.vertices-center)*factor)


def flat_polygon(walls,height,texture):
	"""Creates a flat Polygon with the shape of the walls at the given height
	Parameters
	----------
	- walls  :  procedural_city_generation.building_generation.Walls object
	- height : z coordinate of the polygon to be created
	- texture : procedural_city_generation.building_generation.Texture object
	Returns
	----------
	- procedural_city_generation.building_generation.Polygon3D object

	"""
	return Polygon3D(walls.vertices+np.array([0,0,height]),range(walls.l),texture)


def buildwalls(walls,bottom,top, texture):
	"""Creates one walls Polygon object with shared vertices in the shape of the walls object
	Parameters
	----------
	- walls  :  procedural_city_generation.building_generation.Walls object
	- bottom : float,z coordinate of the bottom of the walls
	- top : float,z coordinate of the top of the walls
	- texture : procedural_city_generation.building_generation.Texture object
	Returns
	----------
	- procedural_city_generation.building_generation.Polygon3D object
	
	Example
	----------
	>>>w=Walls([[0,0,0],[0,1,0],[1,1,0]],3)
	>>>p= buildwalls(  w , 1, 2, some_tex)
	>>>p.verts
	[[0,0,1],[0,1,1],[1,1,1],[0,0,2],[0,1,2],[1,1,2]]
	>>>p.faces
	[[1,0,3,4], [2,1,4,5], [2,0,3,5]]
	
	"""
	verts=np.concatenate((walls.vertices+np.array([0,0,bottom]),walls.vertices+np.array([0,0,top])))
	faces=[[i+1,i,i+walls.l,i+1+walls.l] for i in range(walls.l)-1]
	faces.append([walls.l-1,0,walls.l,2*walls.l-1])
	return Polygon3D(verts,faces,texture)


def buildledge(walls,bottom,top,texture):
	"""Creates one ledge Polygon object with shared vertices in the shape of the walls object
	Parameters
	----------
	- walls  :  procedural_city_generation.building_generation.Walls object
	- bottom : float,z coordinate of the bottom of the walls
	- top : float,z coordinate of the top of the walls
	- texture : procedural_city_generation.building_generation.Texture object
	Returns
	----------
	- procedural_city_generation.building_generation.Polygon3D object
	
	Example
	----------
	>>>w=Walls([[0,0,0],[0,1,0],[1,1,0]],3)
	>>>p= buildlege(  w , 1, 2, some_tex)
	>>>p.verts
	[[0,0,1],[0,1,1],[1,1,1],[0,0,2],[0,1,2],[1,1,2]]
	>>>p.faces
	[[1,0,3,4], [2,1,4,5], [2,0,3,5],[0,1,2],[3,4,5]]
	"""
	verts=np.concatenate((walls.vertices+np.array([0,0,bottom]),walls.vertices+np.array([0,0,top])))
	faces=[[i+1,i,i+walls.l,i+1+walls.l] for i in range(walls.l)-1]
	faces.extend([walls.l-1,0,walls.l,2*walls.l-1], range(walls.l), range(walls.l,2*walls.l))
	return Polygon3D(verts,faces,texture)


def get_window_coords(walls,list_of_currentheights,floorheight, windowwidth, windowheight, windowdist):
	'''
	verts=np.array([])
	faces=[]
	for wall in walls.walls:
		l=np.linalg.norm(np.diff(wall)
		
		
		n=l//(windowwidth+windowdist)
		if n>0:
			v=wall[1]-wall[0]
			vn=v/np.linalg.norm(v)
			
			h=np.array([0,0,windowheight])
			
			
			#Creates a stencil, which, when added to the center point of
			# a window, is a numpy array with shape 4 describing the 
			#window's coordinates
			stencil=np.array([
							(-windowwidth*vn)-h,
							(windowwidth*vn)-h,
							(windowwidth*vn)+h,
							(-winddowwith*vn)+h
							])
			stencilarray=np.array([stencil+np.array([0,0,curr_h]) for curr_h in list_of_currentheights])
			
			for i in range(n):
				center_of_window=wall[0]+(i/(n+1))*v
				np.concatenate(verts,stencilarray+center_of_window)
				
				
				
				
		elif l/windowwidth>=1:
			
			np.array(		[(-windowwidth*vn)-h,
							(windowwidth*vn)-h,
							(windowwidth*vn)+h,
							(-winddowwith*vn)+h
							])
			#TODO
	'''
	
	windows=[]
	for wall in walls:
		for i in range(len(wall)-1):
			
			#TODO comment, fix, and understand this function

			v=wall[i]-wall[i+1]
			l=np.linalg.norm(v)
			n=int(l//( windowwidth+ windowdist))
			if n>0:
				windows.extend(place_windows_on_wall(n,wall[i+1],v,l, windowwidth, windowheight))
				
			elif l// windowwidth>0:
				windows.extend(place_windows_on_wall(1,wall[i+1],v,l, windowwidth, windowheight))
	return windows

def place_windows_on_wall(n,p,v,l,width,height):
	vnorm=v/l
	h=np.array([0,0,height])
	windows=[]
	for i in range(n):
		base=p+(i+1)/(n+1)*v
		base=np.array([base[0],base[1],0])
		windows.append([base-(width*vnorm)/2-h/2,base -(width*vnorm)/2+h/2, base+width*vnorm/2+h/2, base+width*vnorm/2-h/2])
	return windows
	
	
def verticalsplit(height,floorheight):
	'''Splits the Building vertically and returns a list of chars where:
	l=ledge
	f=floor
	b=base (Erdgeschoss)
	r=roof
	'''
	#List of chars to be returned
	returnlist=['b']
	
	#Finds maximum number of floors which fit in. -1 because the first floor is the base
	nfloors=int(height//floorheight)-1
	
	#Finds maximum amount of ledges
	rest=height%floorheight
	nledges=int(rest//(floorheight/10.))
	
	#If there is at least 1 ledge, create it after the basement
	if nledges>0:
		nledges-=1
		returnlist.append('l')
	
	#If there is 1 ledge left, create it at the very top and return returnlist.
	if nledges==1:
		nledges-=1
		for i in range(nfloors):
			returnlist.append('f')
		returnlist.append('l')
		returnlist.append('r')
		return returnlist
	
	#Finds how many floors per ledge are to be created
	factor=np.inf
	if nledges>0:
		factor=int(nfloors//nledges)
	last=True
	
	i=0
	while nfloors>=0:
		returnlist.append('f')
		nfloors-=1
		i+=1
		#If index is multiple of factor, add a ledge
		if factor>0 and i%factor==0 and factor<3:
			returnlist.append('l')
	if returnlist[-1]!='l':
		returnlist.append('l')
	returnlist.append('r')
	return returnlist
	



def scaletransform_vertex(coords,factor,center,p,fac2=None):
	'''To be applied only to Buildings with 4 Sides, before adding any cuts'''
	#TODO: Broken as fk
	if len(coords)>4:
		return scale(coords,factor,center)
	coords=copy(coords)
	
	newcoords=[]
	v_transform=None
	for i in range(len(coords)):
		v=(coords[i]-center)
		if i==p:
			v_transform=v*(1-factor)
		newcoords.append(center+factor*v)
	
	if fac2 is None:
		fac2=np.random.uniform(0,1)
	return [x+fac2*v_transform for x in newcoords]
	
	
def scalewallstransform_vertex(walls,factor,center,p,fac2=None):
	'''To be applied only to Buildings with 4 Sides, before adding any cuts'''
	#TODO: ven brokener than fk
	walls=copy(walls)
	newwalls=[]
	v_transform=None
	for i in range(len(walls)):
		v=(walls[i][0]-center)
		if i==p:
			v_transform=v*(1-factor)
		newwalls.append([center+factor*v])
	
	if fac2 is None:
		fac2=np.random.uniform(0,1)
	
	return [x+fac2*v_transform for x in newwalls]
