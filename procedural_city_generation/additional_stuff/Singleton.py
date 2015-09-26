class Singleton:
	"""
	Singleton Object which can only have one instance.
	Is instanciated with a modulename, e.g. "roadmap", and reads the 
	corresponding "roadmap.conf" in procedural_city_generation/inputs.
	All attributes are mutable, however this class should mainly be used for
	immutable numeric values to avoid confusion/difficult-to-trace-bugs.
	"""
	
	class __Singleton:
		def __init__(self,modulename=None):
			import procedural_city_generation
			import os
			import json
			if modulename:
				path=os.path.dirname(procedural_city_generation.__file__)
				with open(path+"/inputs/"+modulename+".conf",'r') as f:
					d=json.loads(f.read())
				for k,v in d.items():
					setattr(self,k,v)
			else:
				print( "Warning, Singleton instanciated without parsing a json file. Please specify the modulename parameter to avoid errors")
	instance=None
	def __init__(self,modulename=None):
		"""
		Creates the instance.
		
		Parameters
		----------
		modulename : String
		
		"""
		if not Singleton.instance:
			Singleton.instance=Singleton.__Singleton(modulename)
	
	def __getattr__(self,name):
		return getattr(self.instance,name)
		
	def __setattr__(self,name,value):
		setattr(self.instance,name,value)

	def kill(self):
		"""
		Deletes the Singleton's instance
		"""
		Singleton.instance = None
