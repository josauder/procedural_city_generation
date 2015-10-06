import importlib
import pkgutil


def import_submodules(package, recursive=True):
	""" Import all submodules of a module, recursively, including subpackages
	:param package: package (name or actual module)
	:type package: str | module
	:rtype: dict[str, types.ModuleType]
	"""
	
	if isinstance(package, str):
		package = importlib.import_module(package)
	results = {}
	for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
		full_name = package.__name__ + '.' + name
		try:
			results[full_name] = importlib.import_module(full_name)
		except:
			pass
		if recursive and is_pkg:
			results.update(import_submodules(full_name))
	return results

def main():
	import os, sys
	sys.path.append(os.path.dirname(__file__)+"..")
	import procedural_city_generation
	
	a=import_submodules(procedural_city_generation).items()
	a=[x for x in a if "test" in x[0]]
	print a
	

if __name__ == '__main__':
	main()
