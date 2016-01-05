from __future__ import division
import random
import numpy as np
from copy import copy
import procedural_city_generation
from procedural_city_generation.building_generation.Polygon3D import Polygon3D
from procedural_city_generation.building_generation.main import gui as maingui

if maingui is not None:
	plt=maingui
else:
	import matplotlib.pyplot as plt


def walls_from_poly(poly2d):
	"""
	Creates a wall object from a Polygon3D Object by converting 
	Poly.vertices from 2D-Arrays to 3D, np.array([x,y])->np.array([x,y,0])
	
	Parameters
	----------
	poly2d : procedural_city_generation.polygons.Polygon2D object
	
	Returns
	-------
	walls : procedural_city_generation.building_generation.Walls object
	
	"""
	l=len(poly2d.vertices)
	return Walls(np.hstack((np.array(poly2d.vertices),[[0]]*l)),l)


class Walls(object):
	"""
	Walls object which has vertices saved as numpy arrays
	"""
	def __init__(self,verts,l):
		"""
		Parameters
		----------
		verts: numpy.ndarray(l,3)
		l: int
			shape[0] of verts
		"""
		self.vertices=verts
		self.l=l
		self.center=sum(self.vertices)/self.l
		self.walls=None
		
	def getWalls(self):
		"""
		Lazily evaluated walls as numpy array with shape (self.l,2,3)
		
		Returns
		-------
		np.ndarray(l,3,2)
		"""
		if self.walls  is None:
			self.walls= np.array([self.vertices[[i,i-1]] for i in range(self.l)])
		return self.walls

	def selfplot(self):
		"""
		Plots itself with matplotlib

		Returns
		--------
		None
		"""
		c=random.choice("rgbcmyk")
		composite=np.array([x for x in self.vertices]+[self.vertices[0]])
		plt.plot(composite[:,0],composite[:,1],color=c)

def scale(walls,factor):
	"""
	Scales a walls object by a factor
	
	Parameters
	----------
	walls  :  procedural_city_generation.building_generation.Walls object
	factor :  float
		Number to be scaled to. E.g. 2 doubles the size, 0.5 halves the size
	
	Returns
	-------
	walls : procedural_city_generation.building_generation.Walls object
	"""
	return Walls(walls.center+(walls.vertices-walls.center)*factor,walls.l)


def flat_polygon(walls,height,texture):
	"""
	Creates a flat Polygon with the shape of the walls at the given height
	
	Parameters
	----------
	walls : procedural_city_generation.building_generation.Walls object
	height : float
		Z coordinate of the polygon to be created
	texture : procedural_city_generation.building_generation.Texture object
	
	Returns
	-------
	procedural_city_generation.building_generation.Polygon3D object

	"""
	return Polygon3D(walls.vertices+np.array([0,0,height]),[range(walls.l)],texture)


def buildwalls(walls,bottom,top, texture):
	"""Creates one walls Polygon object with shared vertices in the shape of the walls object
	
	Parameters
	----------
	walls  :  procedural_city_generation.building_generation.Walls object
	bottom : float
		Z coordinate of the bottom of the walls
	top : float
		Z coordinate of the top of the walls
	texture : procedural_city_generation.building_generation.Texture object
	
	Returns
	-------
	procedural_city_generation.building_generation.Polygon3D object
	
	Example
	-------
	>>>w=Walls([[0,0,0],[0,1,0],[1,1,0]],3)
	>>>p= buildwalls(  w , 1, 2, some_tex)
	>>>p.verts
	[[0,0,1],[0,1,1],[1,1,1],[0,0,2],[0,1,2],[1,1,2]]
	>>>p.faces
	[[1,0,3,4], [2,1,4,5], [2,0,3,5]]
	
	"""
	verts=np.concatenate((walls.vertices+np.array([0,0,bottom]),walls.vertices+np.array([0,0,top])))
	faces=[[i+1,i,i+walls.l,i+1+walls.l] for i in range(walls.l-1)]
	faces.append([walls.l-1,0,walls.l,2*walls.l-1])
	return Polygon3D(verts,faces,texture)


def buildledge(walls,bottom,top,texture):
	"""
	Creates one ledge Polygon object with shared vertices in the shape of the walls object
	
	Parameters
	----------
	walls  :  procedural_city_generation.building_generation.Walls object
	bottom : float
			z coordinate of the bottom of the walls
	top : float
			z coordinate of the top of the walls
	texture : procedural_city_generation.building_generation.Texture object
	
	Returns
	-------
	procedural_city_generation.building_generation.Polygon3D object
	
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
	faces=[[i+1,i,i+walls.l,i+1+walls.l] for i in range(walls.l-1)]
	faces.extend([[walls.l-1,0,walls.l,2*walls.l-1], range(walls.l), range(walls.l,2*walls.l)])
	return Polygon3D(verts,faces,texture)


def get_windows(walls,list_of_currentheights,floorheight, windowwidth, windowheight, windowdist,texture):
	"""
	Creates a Polygon3D Object containing the coordinates to all windows of a building
	
	Parameters
	----------
	walls  : procedural_city_generation.building_generation.Walls Object
	list_of_currentheights : list<float> 
		Which has one entry for each z-coordinate of a row of windows to be created.
		This always means the 'bottom' of each floor.
	floorheight  :  float
		Floorheight of the building, used to calculate center of each floor where windows are to be built
	windowwidth : float
		Width of each window
	windowheight : float
		Height of each window
	windowdist : float
		Distance between two windows if more than one window fits on the wall
	
	Returns:
	--------
	procedural_city_generation.building_generation.Polygon3D object with shared vertices
	"""
	
	nc=len(list_of_currentheights)
	
	#Start off as empty list
	verts=[]
	
	#Counts number of faces
	nfaces=0
	
	for wall in walls.getWalls():
		
		#l = Length of wall
		l=np.linalg.norm(np.diff(wall,axis=0))
		
		# If at least one window fits into the wall:
		if l>windowwidth:
			
			
			v=wall[1]-wall[0]
			vn=v/np.linalg.norm(v)
			h=np.array([0,0,windowheight/2])
			
			#Creates a stencil, which, when added to the center point of
			# a window, is a numpy array with shape 4 describing the 
			#window's coordinates
			stencil=np.array([
							(-windowwidth/2*vn)-h,
							(windowwidth/2*vn)-h,
							(windowwidth/2*vn)+h,
							(-windowwidth/2*vn)+h
							])
			
			#Stencil for each currentheight in list_of_currentheights
			stencilarray=np.array([stencil+np.array([0,0,curr_h+floorheight/2]) for curr_h in list_of_currentheights])
			
			#If at least one window plus the distance between two windows fits on this wall
			n=int(l/(windowwidth+windowdist))
			
	
			
			if n>0:
				#Then, build a window for the amount of windows that fit on this wall
				nfaces+=n*nc
				for i in range(n):					
					center_of_window=wall[0]+((i+1)/(n+1))*v
					
					verts.extend(np.reshape(stencilarray+center_of_window,(nc*4,3)))

			#Else build one window in the center of the wall
			elif l/windowwidth>1: 
				
				nfaces+=nc
				
				verts.extend(np.reshape(stencilarray+(wall[0]+(0.5*v)),(nc*4,3) ))
	
	#Each window has 4 vertices.
	faces=[range(4*x,4*x+4) for x in range(nfaces)]
	return Polygon3D(verts,faces,texture)
	
	
def verticalsplit(buildingheight,floorheight):
	"""
	Splits the Building vertically.
	
	Parameters
	----------
	buildingheight  : float
		Height of the building
	floorheight  :  float
		Height of each floor
	
	Returns
	-------
	list<char>
		Each character stands for one "building element" where: 
		l=ledge
		f=floor
		b=base (Erdgeschoss)
		r=roof
	"""
	
	#List of chars to be returned. Starts with base
	returnlist=['b']
	
	#Finds maximum number of floors which fit in. -1 because the first floor is the base
	nfloors=int(buildingheight//floorheight)-1
	
	#Finds maximum amount of ledges
	rest=buildingheight%floorheight
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
	
	
	
def scaletransform(walls,scalefactor,transformfactor=None,side=None):
	""" 
	Scales and transforms a procedural_city_generation.building_generation.Walls object
	
	Parameters
	----------
	walls :  procedural_city_generation.building_generation.walls object
	scalefactor : float
		The factor to which the walls object is scaled down to
	transformfactor (optional) : float
		The factor to which the scaled down object will be moved
		to one of the vertices, i.e. 1 means all the way to the vertex, 
		0 means the object will stay centered 
	side (optional) : int
		The vertex to which the object is transformed towards
	
	Returns
	-------
	procedural_city_generation.building_generation.walls object
	"""
	newwalls=scale(walls,scalefactor)
	side=side if side else random.randint(0,walls.l-1)
	transformfactor=transformfactor if transformfactor else random.uniform(0,1)
	v_rest=(newwalls.vertices[side]-walls.vertices[side])*transformfactor
	return Walls(newwalls.vertices+v_rest,walls.l)
