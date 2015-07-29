from __future__ import division
import sys,os
import numpy as np

import procedural_city_generation
path=os.path.dirname(procedural_city_generation.__file__)
from procedural_city_generation.building_generation.cuts import *
from procedural_city_generation.building_generation.roofs import roof
from procedural_city_generation.building_generation import surface
from procedural_city_generation.building_generation import getBuildingHeight as gb
from procedural_city_generation.building_generation.updateTextures import updateTextures, textureGetter
from procedural_city_generation.building_generation.getFoundation import getFoundation

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
	
	polygons=[]
	for poly in polylist:
		
		
		
		
		#Builds the floor. If the Polygon is not a building, there is obviously no need for walls/windows/roofs
		if poly.poly_type == "road" :
			floortexture= roadtexture
			
			polygons.append(Polygon([np.array([x[0],x[1],0]) for x in poly.vertices],
			range(len(poly.vertices)),
			floortexture, True))
			
		elif poly.poly_type == "vacant":
			floortexture=  texGetter.getTexture('Floor',0)
			
			polygons.append(Polygon([np.array([x[0],x[1],0]) for x in poly.vertices],
			range(len(poly.vertices)),
			floortexture, True))
			
		elif poly.poly_type == "lot":
			center=sum(poly.vertices)/len(poly.vertices)
			
			buildingheight= gb.getBuildingHeight(center)
			
			base_h_low,base_h_high= surface.getSurfaceHeight(poly.vertices)
			
			polygons.append(Polygon([np.array([x[0],x[1],0]) for x in poly.vertices],
			range(len(poly.vertices)),
			floortexture, True))
			
			floorheight=np.random.uniform(0.03,0.04)
			floortexture=texGetter.getTexture('Floor',buildingheight/100.)
			windowtexture=texGetter.getTexture('Window',buildingheight/100.)
			walltexture=texGetter.getTexture('Wall',buildingheight/100.)
			rooftexture=texGetter.getTexture('Roof',buildingheight/100.)
			windowwidth=random.uniform(0.01,0.02)
			if buildingheight<0.15: # haus:
				windowheight=random.uniform(0.015, floorheight)
				windowdist=random.uniform(0.015, windowwidth+0.01)
			else:
				windowheight=random.uniform(0.015,0.02)
				windowdist=random.uniform(0, windowwidth+0.05)
			
			#Scales and Translates floor
			if poly.is_convex:
				poly=getFoundation(poly)
			else:
				poly=getFoundation(poly)
				
			
			
			#Need to sort out data structure make it 3D and stuff
			
			poly.vertices=[np.array([x[0],x[1],0]) for x in poly.vertices]
			walls=[[poly.vertices[i-1],poly.vertices[i]] for i in range(len(poly.vertices))]
			print walls
			#Creates floorplan
			walls=randomcut(walls)
			
			#Floor-height is found and the Building is vertically split.
			#TODO: Constants in some sort of conf file
			plan=verticalsplit(buildingheight,floorheight)
			
			#Random, decides if ledges will be scaled nach aussen
			#TODO: add constants to some sort of conf file
			ledgefactor=1.0
			if random.randint(0,100)>50:
				ledgefactor+=random.uniform(0,0.1)
			
			#Scales the walls to the outside
			ledge=scalewalls(walls,ledgefactor)
			
			#Keeps track of height where we are currently building
			currentheight=0
			
			#Get a list of windows for each floor
			windows=get_window_coords(walls,windowtexture,windowwidth,windowheight,windowdist)
			
			#Goes through the plan list
			#TODO: check with desktop version
			for element in plan:
				if element=='b' or element=='f':
					window_coords=scale([x+np.array([0,0,base_h_high+currentheight+floorheight/2]) for x in windows],1.01,grundrisscenter)
					polygons.extend(Polygon(window,range(len(window)),windowtexture) for window in windows)
					currentheight+=floorheight
					
				elif element=='l':
					
					currentheight+=floorheight/10.
					if ledgefactor!=1:
						polygons.append(flatebene(ledge,base_h_high+currentheight,rooftexture))
						polygons.append(flatebene(ledge,base_h_high+currentheight-floorheight/10.),rooftexture)
						polygons.extend(buildwalls(ledge,base_h_high+currentheight-floorheight/10., base_h_high+currentheight,rooftexture))			
				elif element=='r':
					if ledgefactor==1:
						polygons.extend(dach(walls,scale(roofwalls,1.05,grundrisscenter),haus,base_h_high+currentheight,rooftexture))
						polygons.extend(buildwalls(walls,base_h_low,(base_h_high+currentheight),walltexture))
		else:
			print "Polygon.poly_type not understood"
	
	
	
	
	#Groups Polygons with identical Texture 
	poly_group_by_texture=np.zeros(len(textures))
	for poly in polygons:
		mergedpolys[poly.texture.index].append(poly)
	
	
	mergedpolys=[]
	#For each group of polygons with an identical Texture
	ind=0
	for polys in poly_group_by_texture:
		
		#For each polygon in that group
		allverts=[]
		for poly in polys:
			#For each vertex in that polygon
			for vert in poly:
				
				#Add to list of all vertices
				allverts.append(vert)
		
		#Sorts all Vertices
		allverts.sort(key=itemgetter(0,1,2))
		
		#Removes all duplicates
		popindex=0
		for i in range(len(allverts)):
			if np.allclose(allverts[i-popindex],allverts[i-1-popindex]):
				allverts.pop(i-popindex)
				popindex+=1
		print popindex + " duplicates in list of all vertices were removed"
		
		
		
		faces=[]
		def search(x):
			return allverts.index(x)
		
		for poly in polys:
			face=[search(x) for x in poly.vertices]
			faces.append(face)
		
		
		mergedpolys.append(Polygon(allverts,faces,textures[ind]))
		ind+=1
	
	
	
	import pickle,os
	with open(os.path.dirname(procedural_city_generation.__file)+"/outputs/buildings.txt",'w') as f:
		f.write(pickle.dumps(mergedpolys))
	
	
	
	
if __name__ == '__main__':
	main([])
