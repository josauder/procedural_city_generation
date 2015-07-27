#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division


def main():
	from procedural_city_generation.roadmap.config import config
	from copy import copy
	
	
	variables,Global_Lists=config()
	
	front=copy(Global_Lists.vertex_list)
	front.pop(0)
	front.pop()
	vertex_queue = copy(Global_Lists.vertex_queue)
	from iteration import iteration
	variables.iterationszaehler=0
	
	
	if variables.plot==1:
		
		import matplotlib.pyplot as plt
		import matplotlib
		import matplotlib.lines
		from matplotlib.lines import Line2D
		fig=plt.figure()
		ax=plt.subplot(111)
		
		fig.canvas.draw()
		ax.set_xlim((-variables.border[0],variables.border[0]))
		ax.set_ylim((-variables.border[1],variables.border[1]))
	i=0
	while (front!=[] or Global_Lists.vertex_queue	!=[]):
		
		i+=1
		front=iteration(front)
		
		if variables.plot==1:
			if i%variables.plotabstand==0:	
				plt.pause(0.001)
				fig.canvas.blit(ax.bbox)
				fig.canvas.flush_events()
			variables.iterationszaehler=0
	from procedural_city_generation.additional_stuff.jsontools import save_vertexlist
	
	
	print "Roadmap is complete"
	save_vertexlist(Global_Lists.vertex_list,"output",variables.savefig)
	return Global_Lists.vertex_list
	
	
if __name__ == '__main__':
	import os, sys
	parentpath=os.path.join(os.getcwd(),("../../"))
	sys.path.append(parentpath)
	import procedural_city_generation
	
	
	main()
	
