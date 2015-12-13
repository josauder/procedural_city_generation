from __future__ import division
import sys
from parent_path import parent_path
sys.path.append(parent_path(depth=3))
class Variables:
	'''Singleton-Object'''
	
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
		
def config():
	'''Makes all necessary setups in order to run the polygon-generator'''
	import json
	from collections import namedtuple
	import os
	import procedural_city_generation
	
	path=os.path.dirname(procedural_city_generation.__file__)
	try:
		with open(path+"/inputs/polygons.conf",'r') as f:
			variables_string=f.read()
	except:
		raise Exception("Bla")
	variables=json.loads(variables_string,object_hook= lambda d: namedtuple('X',d.keys())(*d.values()))
	variables=Variables(variables)
	return variables
	

if __name__=="__main__":
	print(config())

	
	
	
	
	
	
