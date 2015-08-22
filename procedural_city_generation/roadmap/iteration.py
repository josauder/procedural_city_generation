# -*- coding: utf-8 -*-
from __future__ import division
from procedural_city_generation.roadmap.getSuggestion import getSuggestion
from procedural_city_generation.roadmap.check import check
from config import Global_Lists, Variables

try:
	#In try-except because sphinx fails to document otherwise
	Global_Lists = Global_Lists()
	variables = Variables()
except:
	pass


def iteration(front):
	"""
	Gets Called in the mainloop.
	Manages the front and newfront and the queue
	
	Parameters
	----------
	front : list<Vertex>
	
	Returns
	-------
	newfront : list<Vertex>
	
	"""
	newfront=[]
	
	for vertex in front:
		for suggested_vertex in getSuggestion(vertex):
			newfront=check(suggested_vertex,vertex,newfront)
			
	#Increments index of each element in queue
	Global_Lists.vertex_queue=[[x[0],x[1]+1] for x in Global_Lists.vertex_queue]
	
	#Finds elements in queue which are to be added into the newfront
	while Global_Lists.vertex_queue!=[] and Global_Lists.vertex_queue[0][1]>=variables.minor_road_delay:
		newfront.append(Global_Lists.vertex_queue.pop(0)[0])
	
	return newfront
