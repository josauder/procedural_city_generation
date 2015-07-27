path="/home/jonathan/procedural_city_generation/"
import sys
sys.path.append(path)

from procedural_city_generation.building_generation.cuts import *
from procedural_city_generation.building_generation.roofs import roof
from procedural_city_generation.building_generation import surface
from procedural_city_generation.building_generation import getBuildingHeight as gb
from procedural_city_generation.building_generation.updateTextures import updateTextures

#Poly:
	#is_convex
	#is_Lot
	#is_Road

#define
house_height=0.15
roadtex_name='Road01.jpg'

def main(polylist):
	
	
	textures=updateTextures()
	roadtexture=[x for x in textures if x.name==roadtex_name][0]
	
	
	
	for poly in polylist:
		
		baseheight= surface.getSurfaceHeight(poly)
		buildingheight= gb.getBuildingHeight(center)
		
		basetexture=None
		if poly.road:
			basetexture= roadtexture
		else:
			
		
		
		
		
		
		buildbase(poly)
		
	
	
#	for g in grund_list:
#		if plotbool:
#			g.selfplot()
#		h=getBuildingheight(g.punkte,border)
#		
#		from surface import getHeight
#		
#		minh,maxh=getHeight(g.punkte)
#		
#		buildings.append([g.punkte,g.punkte,h,np.random.uniform(0.035,0.04),maxh,minh])
		
	
#	print "Buildinggenerator creating", len(buildings), "buildings"
	
	
#	buildinggenerator.main(buildings,grosseflaechen,strassenpoly)
	
#	if plotbool:
#		plt.show()
	
if __name__ == '__main__':
	main([])
