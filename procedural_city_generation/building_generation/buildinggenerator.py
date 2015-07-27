from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import random
from cuts import scale, scalewalls,scaletransform_vertex ,Ccut,Hcut,Xcut,Lcut,Tcut,Zcut,Ycut,KeineAhnungcut,KeineAhnung2cut
from copy import copy
from daecher import dach

		
class Polygon(object):
	def __init__(self,coords,texture):
		self.coords=coords
		self.texture=textures


		
class Building(object):
	def __init__(self,grundstueckcoords,grundrisscoords,height,floorheight,start_of_base_height,start_of_fundament_height):
		'''Building Object where:
		coords = list of numpy arrays
		height= height of the building itself
		floorheight= height of each floor
		start_of_base_height= height where the first floor starts, maximum height of the basement on the surface on which we build
		start_of_fundament_height= height where the walls start, minimum height of the basement on the surface on which we build
		'''
		self.height=height
		self.haus=False
		#Gets window kram right:
		if self.height<0.1:
			self.haus=True
		
		self.floorheight=floorheight
		
		self.grundstueckcoords=grundstueckcoords
		self.grundrisscoords=grundrisscoords
		
		#Calculates centers
		self.grundrisscenter=sum(grundstueckcoords)/len(grundstueckcoords)
		self.grundstueckscenter=sum(grundrisscoords)/len(grundrisscoords)
		
		#Chooses random textures
		self.floortexture=random.choice(floortextures)
		self.walltexture=random.choice(walltextures)
		self.rooftexture=random.choice(rooftextures)
		self.windowtexture=random.choice(windowtextures)
		self.ledgetexture=random.choice(walltextures)
		self.start_of_base_height=start_of_base_height
		self.start_of_fundament_height=start_of_fundament_height
		
		self.windowwidth=random.uniform(0.01,0.02)
		if self.haus:
			self.windowheight=random.uniform(0.015,self.floorheight)
			self.windowdist=random.uniform(0.015,self.windowwidth+0.01)
		else:
			self.windowheight=random.uniform(0.015,0.02)
			self.windowdist=random.uniform(0,self.windowwidth+0.05)
		
		
	def build(self):
		floorpolys=[[np.array([x[0],x[1],0]) for x in self.grundstueckcoords]]
		wallpolys=[]
		roofpolys=[]
		windowpolys=[]
		
		if True:#len(self.grundstueckcoords)<20:
			#Scales the Grundriss of the building correct
			scalefactor=1
			
			coords=None
			if not self.haus: 
				scalefactor=np.random.uniform(0.7,1)
			else:
				scalefactor=np.random.uniform(0.4,0.5)
				
			
			if np.random.uniform(0,1)<0.5:
				coords=scaletransform_vertex(self.grundrisscoords,scalefactor,self.grundrisscenter,random.randint(0,2),random.uniform(0,0.7))
			else:
				coords=scale(self.grundrisscoords,scalefactor,self.grundrisscenter)

			
			#Creates walls as Lists of lists, for now unnoetig but makes implementation of additional house shapes easier
			walls=[[coords[i-1],coords[i]] for i in range(len(coords))]
			roofwalls=copy(walls)
			if len(walls)==4:
				
				n=random.randint(0,100)
				if n>20:
					a1=random.uniform(0,0.4)
					a2=random.uniform(0,0.4)
					if n<35:
						walls=Ccut(walls,a1,a2,0)
					elif n<47:
						walls=Hcut(walls,a1,a2,0)
					elif n<56:
						walls=Xcut(walls,a1,a2,0)
					elif n<68:
						walls=Lcut(walls,a1,a2,0)
					elif n<77:
						walls=Tcut(walls,a1,a2,0)
					elif n<82:
						walls=KeineAhnungcut(walls,a1,a2,0)
					elif n<87:
						walls=KeineAhnung2cut(walls,a1,a2,0)
					else:
						walls=Ycut(walls,a1,a2,0)
			#Recieves plan from verticalsplit function
			plan=verticalsplit(self.height,self.floorheight)
			
			
			#Random, decides if ledges will be scaled nach aussen
			ledgefactor=1.0
			if random.randint(0,100)>50:
				ledgefactor+=random.uniform(0,0.1)
			
			#Scales the walls to the outside
			ledge=scalewalls(walls,ledgefactor,self.grundrisscenter)
			
			#Keeps track of height where we are currently building
			currentheight=0
			
			#Get a list of windows for each floor
			windows=self.getwindowcoords(walls)
			#Goes through the plan list
			while len(plan)>0:
				if plan[0]=='b' or plan[0]=='f':
					
					
					windowpolys.extend(scale([x+np.array([0,0,self.start_of_base_height+currentheight+self.floorheight/2]) for x in windows],1.01,self.grundrisscenter))
					currentheight+=self.floorheight
					
				elif plan[0]=='l':
					
					currentheight+=self.floorheight/10.
					if ledgefactor!=1:
						
						
						roofpolys.append(flatebene(ledge,self.start_of_base_height+currentheight))
						roofpolys.append(flatebene(ledge,self.start_of_base_height+currentheight-self.floorheight/10.))
						wallpolys.extend(buildwalls(ledge,self.start_of_base_height+currentheight-self.floorheight/10., self.start_of_base_height+currentheight))			
				elif plan[0]=='r':
					if ledgefactor==1:
						d=dach(walls,scale(roofwalls,1.05,self.grundrisscenter),self.haus,self.start_of_base_height+currentheight)
						roofpolys.extend(d)
		#					roofpolys.extend(dach1([[coords[i-1],coords[i]] for i in range(len(coords))],0.05))
					wallpolys.extend(buildwalls(walls,self.start_of_fundament_height,(self.start_of_base_height+currentheight)))
				
				plan.pop(0)
	#		print self.start_of_fundament_height, self.start_of_base_height, self.start_of_base_height+currentheight
					
		return roofpolys,windowpolys,wallpolys,floorpolys
	
	
	
	
	def polyliststostring(self,roofpolys,windowpolys,wallpolys,floorpolys):
		savestr="_\n"
		if len(roofpolys)>0:
			savestr+=str(textures.index(self.rooftexture))+"\n"
			for i in roofpolys:
				savestr+=polygon(i)
		if len(windowpolys)>0:
			savestr+=str(textures.index(self.windowtexture))+"\n"
			for i in windowpolys:
				savestr+=polygon(i)
		if len(wallpolys)>0:
			savestr+=str(textures.index(self.walltexture))+"\n"
			for i in wallpolys:
				savestr+=polygon(i)
		savestr+=str(textures.index(self.floortexture))+"\n"
		for i in floorpolys:
			savestr+=polygon(i)
			
		
#		print savestr
		return savestr
	
	
	
	def getwindowcoords(self,walls):
		windows=[]
		for wall in walls:
			for i in range(len(wall)-1):
				v=wall[i]-wall[i+1]
				l=np.linalg.norm(v)
				n=int(l//(self.windowwidth+self.windowdist))
				if n>0:
					windows.extend(placewindow(n,wall[i+1],v,l,self.windowwidth,self.windowheight))
					
				elif l//self.windowwidth>0:
					windows.extend(placewindow(1,wall[i+1],v,l,self.windowwidth,self.windowheight))
		return windows

def flatebene(walls,height):
	poly=[]
	for wall in walls:
		poly.extend([np.array([wall[x+1][0],wall[x+1][1],height]) for x in range(len(wall)-1)])
	
	return poly


def buildwalls(walls,bottom,top):
	returnpolys=[]
	
	for wall in walls:
		for i in range(len(wall)-1):
			returnpolys.append([np.array([wall[i][0],wall[i][1],bottom]),
			np.array([wall[i][0],wall[i][1],top]),
			np.array([wall[i+1][0],wall[i+1][1],top]),
			np.array([wall[i+1][0],wall[i+1][1],bottom])])
		
	return returnpolys


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
	
	
	
				
def placewindow(n,p,v,l,width,height):
	vnorm=v/l
	h=np.array([0,0,height])
	windows=[]
	for i in range(n):
		base=p+(i+1)/(n+1)*v
		base=np.array([base[0],base[1],0])
		windows.append([base-(width*vnorm)/2-h/2,base -(width*vnorm)/2+h/2, base+width*vnorm/2+h/2, base+width*vnorm/2-h/2])
	return windows




#Create list of all textures in /stadt/Visualisierung/Textures folder and sort them by name"
import os
textures=os.listdir(os.getcwd()+"/../Visualisierung/Textures")
rooftextures=[]
floortextures=[]
walltextures=[]
windowtextures=[]
roadtextures=[]
for i in textures:
	if "oof" in i:
		rooftextures.append(i)
	elif "all" in i:
		walltextures.append(i)
	elif "loor" in i:
		floortextures.append(i)
		
	elif "indow" in i:
		windowtextures.append(i)
	elif "oad" in i:
		roadtextures.append(i)

def polygon(coords):
	'''returned eine Zeile mit den Koordinaten als String'''
	savestring=""
	for i in coords:
		
		savestring+=str(i[0])+" "+str(i[1])+" "+str(i[2])+" "
	savestring+="\n"
	return savestring



if __name__ == '__main__':
	inputlist=[[[np.array([0,0,0]),np.array([.3,0,0]),np.array([.3,.3,0]),np.array([0,.3,0])],
	[np.array([0,0,0]),np.array([.3,0,0]),np.array([.3,.3,0]),np.array([0,.3,0])],
	0.2,
	0.03,
	0,
	0]]
	
	
	main(inputlist,[],[])
