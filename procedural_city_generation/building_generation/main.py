from __future__ import division
import sys
import numpy as np

path="/home/jonathan/procedural_city_generation/"
sys.path.append(path)

from procedural_city_generation.building_generation.cuts import *
from procedural_city_generation.building_generation.roofs import roof
from procedural_city_generation.building_generation import surface
from procedural_city_generation.building_generation import getBuildingHeight as gb
from procedural_city_generation.building_generation.updateTextures import updateTextures, textureGetter

#Poly:
	#is_convex
	#is_Lot
	#is_Road

#define
house_height=0.15
roadtex_name='Road01.jpg'


def main(polylist):
	
	
	textures=updateTextures()
	texGetter=textureGetter(textures)
	roadtexture=texGetter.getTexture('Road',50)
	print roadtexture
	
	polygons=[]
	for poly in polylist:
		
		#Builds the floor. If the Polygon is not a building, there is obviously no need for walls/windows/roofs
		if poly.polytype is "minor_road" :
			floortexture= roadtexture
			polygons.append(Polygon(poly.coords,range(len(poly.coords)),floortexture, True)
		elif poly.is_lot:
			floortexture=  texGetter.getTexture('Floor',0)
			polygons.append(Polygon(poly.coords,range(len(poly.coords)),floortexture, True)
		else:
			center=sum(poly.coords)/len(poly.coords)
			buildingheight= gb.getBuildingHeight(center)
			baseheight= surface.getSurfaceHeight(poly)
			floortexture=texGetter.getTexture('Floor',buildingheight/100)
			polygons.append(Polygon(poly.coords,range(len(poly.coords)),floortexture, True)
			
			
			
			#Scales and Translates floor
			if poly.is_convex:
				walls=lennystransform(poly.edges)
			else:
				walls=find_largest_rect(poly.edges)
			
			#Creates floorplan
			walls=randomcut(walls)
			
			#Floor-height is found and the Building is vertically split.
			#TODO: Constants in some sort of conf file
			floorheight=np.random.uniform(0.03,0.04)
			plan=verticalsplit(buildingheight)
			
			#Random, decides if ledges will be scaled nach aussen
			ledgefactor=1.0
			if random.randint(0,100)>50:
				ledgefactor+=random.uniform(0,0.1)
			
			#Scales the walls to the outside
			ledge=scalewalls(walls,ledgefactor,center)
			
			#Keeps track of height where we are currently building
			currentheight=0
			
			#Get a list of windows for each floor
			windows=getwindowcoords(walls)
			
			#Goes through the plan list
			while len(plan)>0:
				if plan[0]=='b' or plan[0]=='f':
					
					
					polygons.extend(scale([x+np.array([0,0,self.start_of_base_height+currentheight+self.floorheight/2]) for x in windows],1.01,self.grundrisscenter))
					currentheight+=self.floorheight
					
				elif plan[0]=='l':
					
					currentheight+=self.floorheight/10.
					if ledgefactor!=1:
						polygons.append(flatebene(ledge,self.start_of_base_height+currentheight))
						polygons.append(flatebene(ledge,self.start_of_base_height+currentheight-self.floorheight/10.))
						polygons.extend(buildwalls(ledge,self.start_of_base_height+currentheight-self.floorheight/10., self.start_of_base_height+currentheight))			
				elif plan[0]=='r':
					if ledgefactor==1:
						polygons.extend(dach(walls,scale(roofwalls,1.05,self.grundrisscenter),self.haus,self.start_of_base_height+currentheight)=
						polys.extend(buildwalls(walls,self.start_of_fundament_height,(self.start_of_base_height+currentheight)))
	
			
			
			
		
	
if __name__ == '__main__':
	main([])
