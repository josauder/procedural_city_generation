
def main():
	import os
	
	with open(os.getcwd()+"/surface.txt", "r" ) as f:
		inputstring=f.read()
	
	coordstring, triangstring=inputstring.split("_\n")
	coords=[]
	for line in [x for x in coordstring.split("\n") if x is not ""]:
		coords.append([float(x) for x in line.split(" ") if x is not ""])
	
	triangs=[]
	for line in [x for x in triangstring.split("\n") if x is not ""]:
		triangs.append([int(x) for x in line.split() if x is not ""])
		
	
	try:
		import bpy
		me=bpy.data.meshes.new('mesh')
		ob=bpy.data.objects.new('mesh',me)
		me.from_pydata(coords,[], triangs)
		me.update(calc_edges=True)
		
		bpy.context.scene.objects.link(ob)
	except:
		pass
	
	

if __name__ == '__main__':
	main()

