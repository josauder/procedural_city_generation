# -*- coding: utf-8 -*-
from getRule import getRule
from procedural_city_generation.roadmap.growth_rules.grid import grid
from procedural_city_generation.roadmap.growth_rules.organic import organic
from procedural_city_generation.roadmap.growth_rules.radial import radial
from procedural_city_generation.roadmap.growth_rules.seed import seed
from procedural_city_generation.roadmap.growth_rules.minor_road import minor_road


def getSuggestion(vertex):
	"""
	Calls each of the actual growth rules, and returns a list of suggested vertices
	
	Parameters
	----------
	vertex : Vertex object
	
	Returns
	-------
	list<Vertex>
	
	
	"""
	suggestions=[]
	rule= getRule(vertex)
	#Grid
	if rule[0] == 0:
		l=grid(vertex,rule[2])
		for x in l:
			suggestions.append(x)
	#Organic
	if rule[0] == 1:
		l=organic(vertex,rule[2])
		for x in l:
			suggestions.append(x)
	#Radial
	if rule[0] == 2:
		
		l=radial(rule[1],vertex,rule[2])
		for x in l:
			suggestions.append(x)
	#minor_road
	if rule[0] == 3:
		l=minor_road(vertex,rule[2])
		for x in l:
			suggestions.append(x)
	#seed
	if rule[0] == 4:
		l=seed(vertex,rule[2])
		for x in l:
			suggestions.append(x)
	return suggestions
