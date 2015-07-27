def save_vertexlist(vertex_list, name="output",savefig=0):	
	print "Output is being saved."
	import json
	import procedural_city_generation

	path="/home/jonathan/procedural_city_generation/procedural_city_generation"
	
	Vertexwb={}	
	for i in range(len(vertex_list)):
		neighboursindizes=[vertex_list.index(x) for x in vertex_list[i].neighbours]
		
		#coords, minor_road, seed, neighboursindizes
		Vertexwb[i]=[(vertex_list[i].coords[0],vertex_list[i].coords[1]),  
		vertex_list[i].minor_road, 
		vertex_list[i].seed,neighboursindizes]
	
	
	with open(path+"/outputs/"+name+".json", 'w') as fp:
		json.dump(Vertexwb, fp)
	
	if savefig==1:
		print "Figure is being saved as" + name +".png"
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
		print "Figure is not being saved as image, if you want to save it, change savefig option in conf.txt"
	print "New File " + name+ ".json created in procedural_city_generation/outputs/ with " , len(vertex_list) , " Vertices "
	
	
	return 0
	


def reconstruct(path=None):
	
	if path is None:
		import os
		import procedural_city_generation
		path=os.path.dirname(procedural_city_generation.__file__)+"/outputs/output.json"
		
	import json
	with open(path,'r') as d:
		data=d.read()
	data=json.loads(data)
	
	from procedural_city_generation.roadmap.Vertex import Vertex
	import numpy as np
	vertex_list=[]
	
	vertex_list=[0]*len(data)
	
	
	for x in data:
		y=data[x]
		k=Vertex(np.array(y[0]))
		k.minor_road,k.seed,k.neighboursindizes=y[1],y[2],y[3]
		vertex_list[int(x)]=k
	
	
	index=0
	for k in vertex_list:
		for x in k.neighboursindizes:
			k.neighbours.append(vertex_list[x])
		k.selfindex=index
		index+=1
		
			
	setliste=[]
	
	
	return vertex_list





if __name__=='__main__':
	k=reconstruct()
	import matplotlib.pyplot as plt
	fig=plt.figure()
	import numpy as np
	for x in w:
		x.selfplot()
	plt.show()
