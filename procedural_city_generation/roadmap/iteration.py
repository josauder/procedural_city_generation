# -*- coding: utf-8 -*-
from __future__ import division
if __name__ == '__main__':
	import main
	main.main()

from procedural_city_generation.roadmap.getSuggestion import getSuggestion
from procedural_city_generation.roadmap.check import check
from config import Global_Lists, Variables

Global_Lists = Global_Lists()
variables = Variables()


def iteration(front):
	
	'''Wird in einer Schleife aufgerufen'''
	neufront=[]
	
	for vertex in front:
		for suggested_vertex in getSuggestion(vertex):
			
			neufront=check(suggested_vertex,vertex,neufront)
			
	#Erhöht Indizes von allen Elementen in der Warteliste um 1
	Global_Lists.vertex_queue=[[x[0],x[1]+1] for x in Global_Lists.vertex_queue]
	
	while Global_Lists.vertex_queue!=[] and Global_Lists.vertex_queue[0][1]>=variables.minor_road_delay:
		neufront.append(Global_Lists.vertex_queue.pop(0)[0])
	
	return neufront










