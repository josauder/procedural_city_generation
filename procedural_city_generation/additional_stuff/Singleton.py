class Singleton:
	class __Singleton:
	
		def __init__(self,modulename):
			import procedural_city_generation
			import os
			import json
			path=os.path.dirname(procedural_city_generation.__file__)
			with open(path+"/inputs/"+modulename+".conf",'r') as f:
				d=json.loads(f.read())
			for k,v in d.items():
				setattr(self,k,v)
	
	
	instance=None
	def __init__(self,modulename=None):
		if not Singleton.instance:
			Singleton.instance=Singleton.__Singleton(modulename)
	
	def __getattr__(self,name):
		return getattr(self.instance,name)
	
