# -*- coding: utf-8 -*-
from __future__ import division
from procedural_city_generation.roadmap.getSuggestion import getSuggestion
from procedural_city_generation.roadmap.check import check
from procedural_city_generation.additional_stuff.Singleton import Singleton

singleton=Singleton("roadmap")

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
	singleton.global_lists.vertex_queue=[[x[0],x[1]+1] for x in singleton.global_lists.vertex_queue]
	
	#Finds elements in queue which are to be added into the newfront
	while singleton.global_lists.vertex_queue!=[] and singleton.global_lists.vertex_queue[0][1]>=singleton.minor_road_delay:
		newfront.append(singleton.global_lists.vertex_queue.pop(0)[0])
	
	return newfront
