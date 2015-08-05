from __future__ import division
import sys,os
import numpy as np

import procedural_city_generation
path=os.path.dirname(procedural_city_generation.__file__)
from procedural_city_generation.building_generation.cuts import *
from procedural_city_generation.building_generation.building_tools import *
from procedural_city_generation.building_generation.roofs import roof
from procedural_city_generation.building_generation.Surface import Surface
from procedural_city_generation.building_generation.BuildingHeight import BuildingHeight
from procedural_city_generation.building_generation.updateTextures import updateTextures, textureGetter
from procedural_city_generation.building_generation.getFoundation import getFoundation
from procedural_city_generation.building_generation.merge_polygons import merge_polygons
from procedural_city_generation.additional_stuff.Singleton import Singleton
from copy import copy

singleton=Singleton("building_generation")

def main(polylist):
	""" Accepts a list of procedural_city_generation.polygons.Polygon objects and ... #TODO
	
	Parameters
	----------
	- polylist\t:\tList<procedural_city_generation.polygons.Polygon>
	"""
	
	
	#TODO: Discuss with lenny how we get the largest polygon out.
	maxl=0
	index=0
	for i in range(len(polylist)):
		if len(polylist[i].vertices)>maxl and polylist[i].poly_type== 'vacant':
			index=i
			maxl=len(polylist[i].vertices)
	polylist.pop(index)
	
	
	gb=BuildingHeight()
	surface=Surface()
	textures=updateTextures()
	texGetter=textureGetter(textures)
	roadtexture=texGetter.getTexture('Road',50)
	
	polygons=[]
	for poly in polylist:
		
		#Determines the floortexture. If the Polygon3D is not a building, there is obviously no need for walls/windows/roofs
		if poly.poly_type == "road" :
			floortexture= roadtexture
		elif poly.poly_type == "vacant":
			floortexture=  texGetter.getTexture('Floor',0)
		elif poly.poly_type == "lot":
			#If poly is a building, get all other necessary textures and numerical values
			center=sum(poly.vertices)/len(poly.vertices)
			buildingheight= gb.getBuildingHeight(center)
			
			floortexture=texGetter.getTexture('Floor',buildingheight)
			windowtexture=texGetter.getTexture('Window',buildingheight)
			walltexture=texGetter.getTexture('Wall',buildingheight)
			rooftexture=texGetter.getTexture('Roof',buildingheight)
			
			floorheight=np.random.uniform(singleton.floorheight_min,singleton.floorheight_max)
			windowwidth=random.uniform(singleton.windowwidth_min,singleton.windowwidth_max)
			
			
			housebool=True if buildingheight<singleton.house_height else False
			
			if housebool:
				windowheight=random.uniform(singleton.windowheight_min,singleton.windowheight_max_house)
				windowdist=random.uniform(0, windowwidth+singleton.windowdist_max_house)
			else:
				windowheight_max= singleton.windowheight_max_house if singleton.windowheight_max_house != 0 else floorheight
				windowheight=random.uniform(singleton.windowheight_min, windowheight_max)
				windowdist=random.uniform(singleton.windowdist_min_not_house, windowwidth+singleton.windowdist_max_not_house)
			
			
			base_h_low,base_h_high= surface.getSurfaceHeight(poly.vertices)
			
			#TODO: Fix after lennys fix
			#Scales and Translates floor
			if poly.is_convex:
				walls_ob = Walls(poly)

			else:
				walls_ob = Walls(poly)
			
			
			
			#TODO: make abhaengig von height
			if housebool:
				walls=scalewalls(walls, random.uniform(singleton.scalefactor_min_house,singleton.scalefactor_max_house))
			else:
				walls=scalewalls(walls, random.uniform(singleton.scalefactor_min_not_house,singleton.scalefactor_max_not_house))
			
			roofwalls=copy(walls)
			
			#Creates floorplan
			walls=randomcut(walls)
			
			#Floor-height is found and the Building is vertically split.
			#TODO: Constants in some sort of conf file
			plan=verticalsplit(buildingheight,floorheight)
			
			#Random, decides if ledges will be scaled nach aussen
			ledgefactor=1.0
			if random.randint(0,100)>singleton.prob_ledge:
				ledgefactor=random.uniform(singleton.ledgefactor_min,singleton.ledgefactor_max)
			
			#Scales the walls to the outside
			ledge=scalewalls(walls,ledgefactor)
			
			#Keeps track of height where we are currently building
			currentheight=base_h_high
			
			#Get a list of windows for each floor
			windows=get_window_coords(scalewalls(walls,1.01),windowwidth,windowheight,windowdist)
			
			#Goes through the plan list
			for element in plan:
				if element=='b' or element=='f':
					currentwindows=windows+np.array([0,0,currentheight+floorheight/2])
					polygons.extend(Polygon3D(window,range(len(window)),windowtexture) for window in currentwindows)
					currentheight+=floorheight
					
				elif element=='l':
					
					currentheight+=floorheight/10.
					if ledgefactor!=1:
						polygons.append(flatebene(ledge,currentheight,rooftexture))
						polygons.append(flatebene(ledge,currentheight-floorheight/10.,rooftexture))
						polygons.extend(buildwalls(ledge,currentheight-floorheight/10., currentheight,rooftexture))			
				elif element=='r':
					if ledgefactor==1:
						polygons.extend(roof(walls,roofwalls,currentheight,housebool,rooftexture,texGetter.getTexture("Roof",buildingheight)))
					
					polygons.extend(buildwalls(walls,base_h_low,currentheight,walltexture))
		else:
			print "Polygon3D.poly_type not understood"
			
		#Builds the floor Polygon
		polygons.append(Polygon3D([np.array([x[0],x[1],0]) for x in poly.vertices],
			range(len(poly.vertices)),
			floortexture))
	
	mergedpolys=merge_polygons(polygons,textures)
	return 0
