
class Param(object):
	def __init__(self, name, default, description, allowed_values):
		self.name=name
		self.default=default
		self.description=description
		self.allowed_values=allowed_values
	
	def __repr__(self):
		return self.name
	
	
