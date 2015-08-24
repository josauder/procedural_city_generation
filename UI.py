import sys,os
import procedural_city_generation
donemessage="\n-----------------------------------------------------------\n\t\tDone, waiting for command\n-----------------------------------------------------------"
path=os.path.dirname(procedural_city_generation.__file__)
sys.path.append(path)

def roadmap():
	from procedural_city_generation.roadmap import main as roadmap_main
	roadmap_main.main()

def polygons():
	from procedural_city_generation.polygons import main as polygon_main
	polygon_main.main(None,False)

def building_generation():
	from procedural_city_generation.building_generation import main as building_generation_main
	import pickle
	with open(path+"/outputs/polygons.txt",'r') as f:
		polygons=pickle.loads(f.read())
	building_generation_main.main(polygons)
	
def visualization():
	os.system("blender --python "+path+"/visualization/blenderize.py")

def main():
	"""
	Thisdoc
	"""
	
	if len(sys.argv)==1:
		print main.__doc__
		return 0
	if "options" in sys.argv[2]:
		os.system("nano ./procedural_city_generation/inputs/"+sys.argv[1]+".conf")
	elif "run" in sys.argv[2]:
		eval(sys.argv[1])()
		print donemessage
			
if __name__=='__main__':
	main()
