import sys, os
import json
sys.path.append("/home/jonathan/procedural_city_generation/")
import procedural_city_generation

class Texture(object):
	def __init__(self,name,scale, index=0):
		self.name=name
		self.scale=scale
		self.index=index
	def __repr__(self):
		return self.name
def updateTextures():
	path=os.path.dirname(procedural_city_generation.__file__)
	teximages=os.listdir(path+"/visualization/Textures/")
	
	with open(path+"/visualization/texTable.json",'r') as f:
		texTable=json.loads(f.read())
		
	#TODO: fill out texTable
	textures=[]
	i=0
	for img in teximages:
		i+=1
		try:
			scale=texTable[img]
		except:
			scale=10
		textures.append(Texture(img,scale,i))
	return textures
