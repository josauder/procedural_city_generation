
import sys, os
import random
import json

class Texture(object):
	"""Texture Object
	Parameters
	----------
	- name\t:\tFull name of image of texture
	- scale\t:\tHow many times the texture is to be scaled down. The larger the number the smaller the texture
	- minP\t:\tMinimum int between 0 and 100 so this texture is considered
	- maxP\t:\tMaximum int between 0 and 100 so this texture is considered
	- shrinkwrap\t:\t boolean describing whether Polygon3Ds with this texture will be projected onto surface.
	"""
	def __init__(self,name,scale,minP,maxP,shrinkwrap=False ,index=0):
		
		self.name=name
		self.scale=scale
		self.minP=minP
		self.maxP=maxP
		self.shrinkwrap=shrinkwrap
		self.index=index
	def __repr__(self):
		return "Tex_"+self.name
		
def updateTextures():
	"""Parses /visualization/Textures/ and compares with /visualization/texTable.json
	
	Parameters
	----------
	- None
	
	Returns
	----------
	- list<procedural_city_generation.building_generation.Texture>
	
	Example
	----------
	>>>updateTextures()
	["Tex_Roof03.jpeg","Tex_Grass01.jpg","Tex_Road01.png"]	
	"""
	
	import procedural_city_generation
	path=os.path.dirname(procedural_city_generation.__file__)
	teximages=os.listdir(path+"/visualization/Textures/")
	
	
	with open(path+"/visualization/texTable.json",'r') as f:
		texTable=f.read()
	texTable=json.loads(texTable)
	
	textures=[]
	i=0
	for img in teximages:
		shrinkwrap=True if (("Road" in img) or ("Floor" in img)) else False
		scale,minP,maxP=texTable[img]
		textures.append(Texture(img,scale,minP,maxP,shrinkwrap,i))
		i+=1

	return textures

class textureGetter(object):
	"""Gets initiated with a list of textures, used for chosing a random texture for a specific buildingHeight
	Parameters
	----------
	- textures : list of procedural_city_generation.visualization.texture objects"""
	
	def __init__(self, textures):
		self.textures=textures
		
	def getTexture(self,name,p):
		"""Returns a random texture for a specific name and buildingHeight p between 1 and 100
		
		Parameters
		----------
		- name \t:\tSubstring which has to be included in returned texture
		- p\t:\tInteger between 1 and 100, 100fold of the buildingheight in meters.
		
		Returns
		----------
		- procedural_city_generation.building_generation.Texture object
		
		Example
		----------
		>>>textureGetter.getTexture("Roof",40)
		Tex_Roof03.jpeg
		"""
		 
		p=max(min(100,p*100),0)
		tex=[x for x in self.textures if name in x.name]
		if tex !=[]:
			tex=[x for x in tex if x.minP<=p<=x.maxP]
			if tex!=[]:
				return random.choice(tex)
			else:
				print "Warning! There is no texture that matches the criterion: "+name+" in texturename AND minP<"+str(p)+"<maxP. \n A random Texture was used!"
				return random.choice(self.textures)
		else:
			print "Warning! There is no texture that matches the criterion: "+name+" in texturename. \n A random Texture was used!"
			return random.choice(self.textures)
