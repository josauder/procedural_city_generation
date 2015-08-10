import numpy as np
import time
import matplotlib.pyplot as plt

def merge_polygons(polygons,textures):
	"""
	Groups Polygon3Ds with identical Texture because Blender's mesh.from_pydata() 
	and bpy.context.scene.objects.link take an increasing amount of time with amount 
	of existingPolygons. Saves Polygons to /outputs/buildings.txt
	
	Parameters
	-----------
	- polygons\t:\tlist<procedural_city_generation.polygons.Polygon2D> 
	\t\t\tList of 2D polygons to be built on
	- textures\t:\tlist<procedural_city_generation.building_generation.Texture>
	\t\t\tList of textures in use
	"""
	print "Merging Polygon3Ds"
	
	#List of Empty Lists is filled up with polygons with corresponding texture
	poly_group_by_texture=[[] for x in range(len(textures))]
	[poly_group_by_texture[poly.texture.index].append(poly) for poly in polygons]
	
	
##############################################################################
# Currently not in Use. Only useful when trying to remove duplicate vertices #
##############################################################################
#	def search(x,tree):
#		return tree.query(x,1)[1]
#	
#	def unique(a):
#		order = np.lexsort(a.T)
#		a = a[order]
#		diff = np.diff(a, axis=0)
#		ui = np.ones(len(a), 'bool')
#		ui[1:] = (diff < 0.01).any(axis=1) 
#		return a[ui]
	
	mergedpolys=[]
	ind=0
	for polys in poly_group_by_texture:
		if len(polys)>0:
			
#### Also not in use, see above ####
#			allverts=[]
#			[allverts.extend(poly.verts) for poly in polys]
#			faces=[]
#			from scipy.spatial import cKDTree
#			tree=cKDTree(allverts,leafsize=32)
#			faces=[[search(vert,tree) for vert in poly.verts] for poly in polys]
			
			M=Merger()
			[M.merge(poly) for poly in polys]
			
			#TODO: Fix Scale!
			savelist=[[x.tolist() for x in M.allverts],M.allfaces,textures[ind].name,textures[ind].scale*30,textures[ind].shrinkwrap]
			mergedpolys.append(savelist)
		ind+=1
	
	print "Merging done, saving data structure"
	import pickle,os
	import procedural_city_generation
	with open(os.path.dirname(procedural_city_generation.__file__)+"/outputs/buildings.txt",'w') as f:
		f.write(pickle.dumps(mergedpolys))
	return 0
	
	
	
class Merger(object):
	"""Merger Class used to Merge polygons together while keeping track of an index"""
	def __init__(self):
		self.n=0
		self.allverts=[]
		self.allfaces=[]
		
	def merge(self,poly):
		"""merges polygons with same Texture
		Parameters
		----------
		- poly\t:\tprocedural_city_generation.building_generation.Polygon3D Object to be merged to this Merger
		
		Example:
		>>>anotherPoly.verts
		[(0,0,0),(0,1,0),(1,1,0)]
		>>>anotherPoly.faces
		[0,1,2]
		>>>m=Merger()
		>>>m.allverts
		[(3,3,0),(3,4,0),(4,4,0)]
		>>>m.faces
		[(0,1,2)]
		>>>m.merge(anotherPoly)
		>>>m.allverts
		[(3,3,0),(3,4,0),(4,4,0),(0,0,0),(0,1,0),(1,1,0)]
		>>>m.faces
		[(0,1,2),(3,4,5)]
		"""
		self.allfaces.extend([[x+self.n for x in face] for face in poly.faces])
		self.n+=len(poly.verts)
		self.allverts.extend(poly.verts)
