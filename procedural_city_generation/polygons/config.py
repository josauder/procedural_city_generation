from __future__ import division

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
		
def config():
	'''Makes all necessary setups in order to run the polygon-generator'''
	import json
	from collections import namedtuple
	import procedural_city_generation
	
	path=os.path.dirname(procedural_city_generation.__file__)
	try:
		with open(path+"/inputs/polygons.conf",'r') as f:
			variables_string=f.read()
	except:
		raise Exception("Bla")
	variables=json.loads(variables_string,object_hook= lambda d: namedtuple('X',d.keys())(*d.values()))
	return variables
	
print config()

if __name__=="__main__"

	
	
	
	
	
	
