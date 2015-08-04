

from __future__ import division
import random
import numpy as np
from copy import copy
import procedural_city_generation
from procedural_city_generation.building_generation.Polygon3D import Polygon3D


def scale(coords,factor,center=None):
	if center == None:
		center=sum(coords)/len(coords)
	coords=center+(np.array(coords)-center)*factor
	return list(center)

def scalewalls(walls,factor,center=None):
	
	#TODO: Fix
	center=sum([x[0] for x in walls])/len(walls)	
	
	walls=copy(walls)
	newwalls=[]
	for wall in walls:
		newwalls.append([center+(coord-center)*factor for coord in wall])
	return newwalls
	

def flatebene(walls,height,texture):
	h=np.array([0,0,height])
	
	poly=[]
	for wall in walls:
		for i in range(len(wall)-1):
			poly.append(wall[i]+h)
		
	return Polygon3D(poly,range(len(poly)),texture)


def buildwalls(walls,bottom,top, texture):
	returnpolys=[]
	
	for wall in walls:
		for i in range(len(wall)-1):
			returnpolys.append([np.array([wall[i][0],wall[i][1],bottom]),
			np.array([wall[i][0],wall[i][1],top]),
			np.array([wall[i+1][0],wall[i+1][1],top]),
			np.array([wall[i+1][0],wall[i+1][1],bottom])])
		
	return [Polygon3D(x,range(len(x)),texture) for x in returnpolys]


def get_window_coords(walls,windowwidth, windowheight, windowdist):
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
