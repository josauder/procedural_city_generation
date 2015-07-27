# -*- coding:utf-8 -*-

from __future__ import division
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import os

class Variables:
	'''Singleton-Object which is created upon parsing of roadmap.json'''
	
	class __Variables:
		def __init__(self,tupel=None):
			for x in tupel._fields:
				setattr(self,x,tupel.__getattribute__(x))
	instance=None
	def __init__(self,tupel=None):

		
		if not Variables.instance:
			Variables.instance=Variables.__Variables(tupel)
	
	def __setattr__(self,name,val):
		setattr(self.instance,name,val)
	
	def __getattr__(self, name):
		return getattr(self.instance,name)
	
class Global_Lists:
	class __Global_Lists:
		def __init__(self):

			self.vertex_list=[]
			self.vertex_queue=[]

	instance=None
	def __init__(self):
		if not Global_Lists.instance:
			Global_Lists.instance=Global_Lists.__Global_Lists()
	def __setattr__(self,name,val):
		setattr(self.instance,name,val)
	
	def __getattr__(self, name):
		return getattr(self.instance,name)
	


def config():
	'''Makes all necessary setups in order to run the roadmap-generator'''
	import json
	from collections import namedtuple
	import os
	
	#TOOD: Check Path
	#path=os.getcwd().replace("/roadmap","")
	import procedural_city_generation
	path=os.path.dirname(procedural_city_generation.__file__)
	#Reads roadmap.conf and creates a namedtuple from the json-file format
	#TODO: switch from JSON format to something more useful which can include comments so the inputs are explained to the user
	try:
		with open(path+"/inputs/roadmap.conf",'r') as f:
			variables_string=f.read()
	except:
		print "roadmap.conf could not be found in " +path+"/inputs/ \n attempting to find it in your download folder"
		try:
			with open(os.getcwd().replace("/roadmap","")+"/roadmap/inputs/roadmap.conf",'r') as f:
				variables_string=f.read()
				
				
		except:
			print "roadmap.conf could not be found there either. Please Enter the path to roadmap.conf (ending in /roadmap.conf), if this path doesn't work the Program will exit"
			conf_path=raw_input(">>")
			try:
				with open(str(conf_path)) as f:
					variables_string=f.read()
			except:
				import sys
				sys.exit(1)
	variables=json.loads(variables_string,object_hook= lambda d: namedtuple('X',d.keys())(*d.values()))
	
	#Creates Singleton-Variables object from namedtuple
	variables=Variables(variables)
	
	from Vertex import Vertex
	#Erstellt Vertex-Objekte aus Koordinaten der Axiome
	#TODO:translate vertex to vertices
	variables.axiom=[Vertex(np.array([float(x[0]),float(x[1])])) for x in variables.axiom]
	
	#Finds the longest possible length of a connection between to vertices
	variables.maxLength=max(variables.radiallMax,variables.gridlMax,variables.organiclMax,variables.minor_roadlMax,variables.seedlMax)
	
	import os
	
	import procedural_city_generation.roadmap.config_functions as config_functions
	variables.img,variables.img2=config_functions.input_image_setup(path+"/inputs/rule_pictures/"+variables.rule_image_name, path+"/inputs/density_pictures/"+variables.density_image_name)
	
	
	#TODO:saubermachen
	variables.zentrum=config_functions.find_radial_centers(variables)
	variables.zentrum= [np.array([variables.border[0]*((x[1]/variables.img.shape[1])-0.5)*2,variables.border[1]*(((variables.img.shape[0]-x[0])/variables.img.shape[0])-0.5)*2]) for x in variables.zentrum]
	
	config_functions.setup_heightmap(variables,path)
	
	
	with open(path+"/temp/border.txt",'w') as f:
		f.write(str(variables.border[0])+" "+str(variables.border[1]))
	
	
	#Erstelt Global_Lists-Objekt mit Dynamischer Vertex- und Wegliste
	from copy import copy
	global_lists=Global_Lists()
	global_lists.vertex_list=copy(variables.axiom)
	global_lists.vertex_queue=[]
	global_lists.coordsliste=[x.coords for x in global_lists.vertex_list]
	
	#Setzt die Nachbarn im Axiom richtig
	#TODO:translate
	def setNachbarn(vertex):
		'''Setzt für jeden vertex im Axiom den richtigen Nachbarn'''
		d=np.inf
		neighbour=None
		for v in variables.axiom:
			if v is not vertex:
				dneu=np.linalg.norm(v.coords-vertex.coords)
				if dneu<d:
					d=dneu
					neighbour=v
		vertex.neighbours=[neighbour]
	
	for k in variables.axiom:
		setNachbarn(k)
		
	from scipy.spatial import cKDTree
	global_lists.tree=cKDTree(global_lists.coordsliste, leafsize=160)
	
	return variables,global_lists
