
from __future__ import division
import random
import numpy as np
from copy import copy
import procedural_city_generation
from procedural_city_generation.building_generation.Polygon import Polygon

def normale(arr):
	if arr.size==2:
		n= np.array([arr[1],-arr[0]])
		return n
	else:
		n=np.array([arr[1],-arr[0],0])
		return n

def scale(coords,factor):
	center=sum(coords)/len(coords)
	coords=center+(np.array(coords)-center)*factor
	return list(center)

def scalewalls(walls,factor,center=None):
	
	center=sum(np.array(walls)[::,1])/len(walls)	
	
	walls=copy(walls)
	newwalls=[]
	for wall in walls:
		newwalls.append([center+(coord-center)*factor for coord in wall])
	return newwalls

def randomcut(walls):
	#TODO: Get numeric values in some sort of conf file
	n=random.randint(0,100)	
	a1=random.uniform(0,0.4)
	a2=random.uniform(0,0.4)
	s=random.randint(0,len(walls)-1)
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
	


def scaletransform_vertex(coords,factor,center,p,fac2=None):
	'''To be applied only to Buildings with 4 Sides, before adding any cuts'''
	#Broken as fk
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
	#Even brokener than fk
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



def flatebene(walls,height,texture,shrinkwrap=False):
	poly=[]
	for wall in walls:
		poly.extend([np.array([wall[x+1][0],wall[x+1][1],height]) for x in range(len(wall)-1)])
	
	return Polygon(poly,range(len(poly)),texture,shrinkwrap)


def buildwalls(walls,bottom,top, texture):
	returnpolys=[]
	
	for wall in walls:
		for i in range(len(wall)-1):
			returnpolys.append([np.array([wall[i][0],wall[i][1],bottom]),
			np.array([wall[i][0],wall[i][1],top]),
			np.array([wall[i+1][0],wall[i+1][1],top]),
			np.array([wall[i+1][0],wall[i+1][1],bottom])])
		
	return [Polygon(x,range(len(x)),texture) for x in returnpolys]


def get_window_coords(walls,windowwidth, windowheight, windowdist):
	windows=[]
	for wall in walls:
		for i in range(len(wall)-1):
			
			#TODO remove
			if i>0:
				print "/cuts.py line 271, index=",i
				
			v=wall[i]-wall[i+1]
			l=np.linalg.norm(v)
			n=int(l//( windowwidth+ windowdist))
			if n>0:
				windows.extend(place_window_on_wall(n,wall[i+1],v,l, windowwidth, windowheight))
				
			elif l// windowwidth>0:
				windows.extend(place_window_on_wall(1,wall[i+1],v,l, windowwidth, windowheight))
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
	


