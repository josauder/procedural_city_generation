def save_vertexlist(vertex_list, name="output",savefig=0):	
	print("Output is being saved.")
	import os
	path=os.getcwd()+"/procedural_city_generation"
		
	import pickle
	try:
		with open(path+"/temp/"+name, "wb") as f:
			import sys
			if sys.version[0]=="2":
				s = pickle.dumps(vertex_list)
				f.write(s)
			else:
				pickle.dump(vertex_list,f)
	except:
		print("Recursionlimit was not enough - Pickle trying again with sys.recusionlimit at 50000")
		sys.setrecursionlimit(50000)
		return save_vertexlist(vertex_list,name, savefig)

	if savefig==1:
		print("Figure is being saved as" + name +".png")
		import matplotlib.pyplot as plt

		for k in vertex_list:
			for n in k.neighbours:
				col='black'
				width=3
				if n.minor_road or k.minor_road:
					col='blue'
					width=1
				
				plt.plot([n.coords[0],k.coords[0]],[n.coords[1],k.coords[1]],color=col, linewidth=width)
		
		
		plt.savefig(path+"/outputs/"+name+".png")
	else:
		print("Figure is not being saved as image, if you want to save it, change savefig option in conf.txt")
	print("New File " + name+ " created in procedural_city_generation/temp/ with " , len(vertex_list) , " Vertices ")
	
	
	return 0
	


def reconstruct(path):
	try:
		import os
		import procedural_city_generation
		fullpath=os.path.dirname(procedural_city_generation.__file__)+"/temp/"+path
		
		import pickle
		with open(fullpath,'rb') as f:
			vertex_list=pickle.loads(f.read())
			for i,v in enumerate(vertex_list):
				v.selfindex=i
			return vertex_list

		print("Input could not be located. Try to run the previous program in the chain first.")
		return 0
	except:
		print("Recursionlimit was not enough - Pickle trying again with sys.recusionlimit at 50000")
		sys.setrecursionlimit(50000)
		reconstruct(path)