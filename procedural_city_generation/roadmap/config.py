# -*- coding:utf-8 -*-

from __future__ import division
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import os

class Global_Lists:
	def __init__(self):
		self.vertex_list=[]
		self.vertex_queue=[]
		self.tree=None

def config():
	"""
	Starts the program up with all necessary things. Reads the inputs,
	creates the Singleton objects properly, sets up the heightmap for later,
	makes sure all Vertices in the axiom have the correct neighbor. Could
	need a rework in which the Singletons are unified and not broken as they
	are now.
	
	Returns
	-------
	variables : Variables object
		Singleton with all numeric values which are not to be changed at runtime
	singleton.global_lists : singleton.global_lists object
		Singleton with the Global Lists which will be altered at runtime
	"""
	import json
	from collections import namedtuple
	import os
	
	import procedural_city_generation
	from procedural_city_generation.additional_stuff.Singleton import Singleton
	path=os.path.dirname(procedural_city_generation.__file__)
	
	singleton=Singleton("roadmap")
	
	#Creates Singleton-Variables object from namedtuple
	
	from procedural_city_generation.roadmap.Vertex import Vertex, set_plotbool
	#Creates Vertex objects from coordinates
	singleton.axiom=[Vertex(np.array([float(x[0]),float(x[1])])) for x in singleton.axiom]
	set_plotbool(singleton.plot)
	
	#Finds the longest possible length of a connection between to vertices
	singleton.maxLength=max(singleton.radiallMax,singleton.gridlMax,singleton.organiclMax,singleton.minor_roadlMax,singleton.seedlMax)
	
	import os
	
	from procedural_city_generation.roadmap.config_functions.input_image_setup import input_image_setup
	singleton.img,singleton.img2=input_image_setup(singleton.rule_image_name, singleton.density_image_name)

	with open (path+"/temp/"+singleton.output_name+"_densitymap.txt",'w') as f:
		f.write(singleton.density_image_name.split(".")[0]+"diffused.png")
	
	from procedural_city_generation.roadmap.config_functions.find_radial_centers import find_radial_centers
	singleton.center=find_radial_centers(singleton)
	singleton.center= [np.array([singleton.border[0]*((x[1]/singleton.img.shape[1])-0.5)*2,singleton.border[1]*(((singleton.img.shape[0]-x[0])/singleton.img.shape[0])-0.5)*2]) for x in singleton.center]
	
	from procedural_city_generation.roadmap.config_functions.setup_heightmap import setup_heightmap
	setup_heightmap(singleton,path)

	
	singleton.global_lists=Global_Lists()
	singleton.global_lists.vertex_list.extend(singleton.axiom)
	singleton.global_lists.coordsliste=[x.coords for x in singleton.global_lists.vertex_list]
	
	def setNeighbours(vertex):
		""" Correctly Sets up the neighbors for a vertex from the axiom.
		
		Parameters
		----------
		vertex : vertex Object
		"""
		
		d=np.inf
		neighbour=None
		for v in singleton.axiom:
			if v is not vertex:
				dneu=np.linalg.norm(v.coords-vertex.coords)
				if dneu<d:
					d=dneu
					neighbour=v
		vertex.neighbours=[neighbour]
	
	for k in singleton.axiom:
		setNeighbours(k)
		
	from scipy.spatial import cKDTree
	singleton.global_lists.tree=cKDTree(singleton.global_lists.coordsliste, leafsize=160)
	
	return singleton
