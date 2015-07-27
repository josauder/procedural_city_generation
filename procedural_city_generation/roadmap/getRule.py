# -*- coding: utf-8 -*-
from __future__ import division
from copy import copy
import numpy as np
from Vertex import Vertex
from config import Variables,Global_Lists


variables=Variables()
Global_Lists=Global_Lists()




def getRule(vertex):
	'''gibt die Rule als Tupel von String, womöglich einem array, und einer Zahl zwischen 0 und 1  wieder'''
	
	
	x = (vertex.coords[0]+variables.border[0])/(variables.border[0]*2)
	y = (vertex.coords[1]+variables.border[1])/(variables.border[1]*2)
	
	population_density = np.sqrt((variables.img2[variables.img2.shape[0]-y*variables.img2.shape[0]][x*variables.img2.shape[1]][0])/255)
	if vertex.seed:
		return (4, None,population_density)
	
	
	if not vertex.minor_road:
		#Berechnet die relative Position des Punktes innerhalb der 
		#Rule-Karte. Gibt abhaengig von den Farbwerten an diesem Punkt
		#eine die zutreffende Rule aus.
		
		intrule=np.argmax(variables.img[variables.img.shape[0]-y*variables.img.shape[0]][x*variables.img.shape[1]])
		z=(0,0)
		
		#Bei Radial, suche das naechste Zentrum
		if intrule == 2:
			z=variables.zentrum[np.argmin(np.linalg.norm(vertex.coords-variables.zentrum,axis=1))]
		return (intrule,z,population_density)
		
		
	
	else:

		return (3, None,population_density)
