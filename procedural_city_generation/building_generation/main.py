from __future__ import division
import sys,os
import numpy as np



gui=None

def main():
	""" Reads list of procedural_city_generation.polygons.Polygon2D objects from file
	and constructs buildings on top of these. The buildings consist of Polygon3D objects,
	which are saved to /outputs/polygons.txt. See merger module for more details.
	"""

	import procedural_city_generation
	path=os.path.dirname(procedural_city_generation.__file__)
	from procedural_city_generation.building_generation.cuts import scale, scaletransform, walls_from_poly, randomcut
	from procedural_city_generation.building_generation.building_tools import Polygon3D, verticalsplit, buildledge, buildwalls, get_windows
	from procedural_city_generation.building_generation.roofs import roof
	from procedural_city_generation.building_generation.Surface import Surface
	from procedural_city_generation.building_generation.BuildingHeight import BuildingHeight
	from procedural_city_generation.building_generation.updateTextures import updateTextures, textureGetter
	from procedural_city_generation.building_generation.merge_polygons import merge_polygons
	from procedural_city_generation.additional_stuff.Singleton import Singleton
	from copy import copy
	singleton=Singleton("building_generation")

	import pickle
	with open(path+"/temp/"+singleton.input_name+"_polygons.txt","rb") as f:
		polylist=pickle.loads(f.read())

	#TODO: Discuss with lenny how we get the largest polygon out.
	maxl=0
	index=0
	for i in range(len(polylist)):
		if len(polylist[i].vertices)>maxl and polylist[i].poly_type== 'vacant':
			index=i
			maxl=len(polylist[i].vertices)
	polylist.pop(index)
	
	
	gb=BuildingHeight(singleton.input_name)
	surface=Surface(singleton.input_name)
	textures=updateTextures()
	texGetter=textureGetter(textures)
	roadtexture=texGetter.getTexture('Road',50)
	
	polygons=[]

	counter=0
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
			windowwidth=np.random.uniform(singleton.windowwidth_min,singleton.windowwidth_max)
			
			
			housebool=True if buildingheight<singleton.house_height else False
			
			if housebool:
				windowheight=np.random.uniform(singleton.windowheight_min,singleton.windowheight_max_house)
				windowdist=np.random.uniform(0, windowwidth+singleton.windowdist_max_house)
			else:
				windowheight_max= singleton.windowheight_max_not_house if singleton.windowheight_max_not_house != 0 else floorheight
				windowheight=np.random.uniform(singleton.windowheight_min, windowheight_max)
				windowdist=np.random.uniform(singleton.windowdist_min_not_house, windowwidth+singleton.windowdist_max_not_house)
			
			
			base_h_low,base_h_high= surface.getSurfaceHeight(poly.vertices)
			
			#TODO: Fix after lennys fix, 
			#Scales and Translates floor
			if poly.is_convex:
				walls = walls_from_poly(poly)
			else:
				walls = walls_from_poly(poly)
			
			
			
			#TODO: make abhaengig von height
			if housebool:
				factor=np.random.uniform(singleton.scalefactor_min_house,singleton.scalefactor_max_house)
				if not poly.is_convex:
					walls=scaletransform(walls,factor)
				
				else:
					walls=scale(walls, factor)
			else:
				factor=np.random.uniform(singleton.scalefactor_min_not_house,singleton.scalefactor_max_not_house)
				if not poly.is_convex:
					walls=scaletransform(walls, factor)
				
				else:
					walls=scale(walls,factor)
					
			roofwalls=copy(walls)
			
			#Creates floorplan
			walls=randomcut(walls,housebool)
			if singleton.plotbool:
				walls.selfplot()

			#Floor-height is found and the Building is vertically split.
			#TODO: Constants in some sort of conf file
			plan=verticalsplit(buildingheight,floorheight)
			
			#Random, decides if ledges will be scaled nach aussen
			ledgefactor=1.0
			if np.random.uniform(0,1)>singleton.prob_ledge:
				ledgefactor=np.random.uniform(singleton.ledgefactor_min,singleton.ledgefactor_max)
			
			#Scales the walls to the outside
			ledge=scale(walls,ledgefactor)
			
			#Keeps track of height where we are currently building
			currentheight=base_h_high
			
			#Get a list of windows for each floor
			windows=scale(walls,1.01)
			
			list_of_currentheights=[]
			
			#Goes through the plan list
			for element in plan:
				if element=='b' or element=='f':
					
					list_of_currentheights.append(currentheight)
					
					currentheight+=floorheight
					
				elif element=='l':
					
					if ledgefactor!=1:
						polygons.append(buildledge(ledge,currentheight,currentheight+floorheight/10,rooftexture))
						
					currentheight+=floorheight/10.
				elif element=='r':
	
					if ledgefactor==1:
						polygons.extend(roof(walls,roofwalls,currentheight,housebool,rooftexture,texGetter.getTexture("Roof",buildingheight)))
					
					polygons.append(buildwalls(walls,base_h_low,currentheight,walltexture))
					
			polygons.append(get_windows(windows,list_of_currentheights,floorheight, windowwidth,windowheight,windowdist,windowtexture))
		else:
			print("Polygon3D.poly_type not understood")
		if singleton.plotbool:
			if counter%singleton.plot_counter==0:
				gui.update()
		counter+=1
		#Builds the floor Polygon
		polygons.append(Polygon3D([np.array([x[0],x[1],0]) for x in poly.vertices],
			[range(len(poly.vertices))],
			floortexture))
	
	mergedpolys=merge_polygons(polygons,textures,singleton.output_name)
	return 0
