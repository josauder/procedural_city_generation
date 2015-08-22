# -*- coding: utf-8 -*-
from __future__ import division
from copy import copy
import numpy as np
from Vertex import Vertex
from config import Variables,Global_Lists

try:
	#In try-except because sphinx fails to document otherwise
	Global_Lists = Global_Lists()
	variables = Variables()
except:
	pass

def getRule(vertex):
	"""
	Gets the correct growth_rule for a Vertex, depending on that objects'
	xy coordinates and the growth_rule_image
	
	Parameters
	----------
	vertex : Vertex object
	
	Returns
	-------
	tuple(int, np.ndarray(3,) , float)
		(int) for choosing the correct growth rule,
		(np.ndarray) for center in case that the radial rule is chosen,
		(float) for population_density
	"""
	x = (vertex.coords[0]+variables.border[0])/(variables.border[0]*2)
	y = (vertex.coords[1]+variables.border[1])/(variables.border[1]*2)
	
	population_density = np.sqrt((variables.img2[variables.img2.shape[0]-y*variables.img2.shape[0]][x*variables.img2.shape[1]][0])/255)
	if vertex.seed:
		return (4, None,population_density)
	
	
	if not vertex.minor_road:
		#Finds the relative position of the vertex on the growth_rule_image
		intrule=np.argmax(variables.img[variables.img.shape[0]-y*variables.img.shape[0]][x*variables.img.shape[1]])
		z=(0,0)
		
		#If the rule is radial, find the closest radial center
		if intrule == 2:
			z=variables.zentrum[np.argmin(np.linalg.norm(vertex.coords-variables.zentrum,axis=1))]
		return (intrule,z,population_density)
	else:
		return (3, None,population_density)
