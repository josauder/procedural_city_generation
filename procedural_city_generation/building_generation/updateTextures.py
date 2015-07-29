import sys, os
import random
import json
sys.path.append("/home/jonathan/procedural_city_generation/")
import procedural_city_generation

class Texture(object):
	def __init__(self,name,scale,minP,maxP ,index=0):
		self.name=name
		self.scale=scale
		self.minP=minP
		self.maxP=maxP
		self.index=index
	def __repr__(self):
		return self.name
		
def updateTextures():
	path=os.path.dirname(procedural_city_generation.__file__)
	teximages=os.listdir(path+"/visualization/Textures/")
	
	
	with open(path+"/visualization/texTable.json",'r') as f:
		texTable=f.read()
	texTable=json.loads(texTable)
		
	#TODO: fill out texTable
	textures=[]
	i=0
	for img in teximages:
		i+=1
		scale,minP,maxP=texTable[img]
		textures.append(Texture(img,scale,minP,maxP,i))
	return textures

class textureGetter(object):
	def __init__(self, textures):
		self.textures=textures
		
	
	def getTexture(self,name,p):
		
		tex=[x for x in self.textures if name in x.name]
		if tex !=[]:
			tex=[x for x in tex if x.minP<p<x.maxP]
			if tex!=[]:
				return random.choice(tex)
			else:
				print "Warning! There is no texture that matches the criterion: "+name+" in texturename AND minP<"+str(p)+"<maxP. \n A random Texture was used!"
				return random.choice(self.textures)
		else:
			print "Warning! There is no texture that matches the criterion: "+name+" in texturename. \n A random Texture was used!"
			return random.choice(self.textures)
