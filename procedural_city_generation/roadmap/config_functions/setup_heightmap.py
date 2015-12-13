import numpy as np
import os
def setup_heightmap(singleton,path):	
	#TODO: Document	
	'''Sets up the heightmap image from roadmap.conf entry heightmap_name, writes ./Heightmaps/inuse.txt so other functions know which heightmap to load
	possible inputs:
	random: generates a new random map with randommap.py
	insert_name
	insert_name.png
	insert_name.txt
	'''
	
	#TODO make inputs more flexible
	name=singleton.heightmap_name


	if name=="random":
		print("New random heightmap is being created with randommap.py")
		#Writes correct inuse.txt
		from procedural_city_generation.additional_stuff import randommap
		randommap.main(singleton.border,path)
		
		with open(path+"/temp/"+singleton.output_name+"_heightmap.txt",'w') as f:
			f.write("randommap_"+str(singleton.border[0])+"_"+str(singleton.border[1]))
		return 0
	
	
	#Writes correct inuse.txt
	with open(path+"/temp/"+singleton.output_name+"_heightmap.txt",'w') as f:
		f.write(name[0:-4]+"_"+str(singleton.border[0])+"_"+str(singleton.border[1]))

	#If a txt has already been written for the input in the image, OR if the input was a .txt to begin with, simply load that txt
	if (name[0:-4]+"_"+str(singleton.border[0])+"_"+str(singleton.border[1]) in os.listdir(path+"/temp/")):
		return 0
	
	#If the given image has no .txt yet, write the corresponding.txt
	
	#Load image and resize
	from PIL import Image
	img = Image.open(path+'/inputs/heightmaps/'+name)    
	
	
	#TODO: set these numbers to some file where they can be edited easier
	rsize = img.resize(((singleton.border[1]+20)*10,(singleton.border[0]+20)*10))
	array = np.asarray(rsize) 
	from copy import copy
	array=copy(array)
	
	
	#If image is a jpeg, all values have to be divided by 255
	array=array[::,:,0]/255.
	
	print("You have selected a heightmap which has no .txt file yet, OR the given .txt file has the wrong dimensions. The parameter heightDif will be used to describe the height difference between the lowest and the highest points on the map.")
	h=singleton.heightDif
	print("Processing image")
	
	
	#TODO: Find and Fix this Bug
	array*=abs(h)
	#Caused weird bugs when -=h was used.. I still can't explain them...
	array-= h+0.01
	
	#Create all necessary stuff for the heightmap
	from scipy.spatial import Delaunay as delaunay
	indices	=	np.vstack(np.unravel_index(np.arange(array.shape[0]*array.shape[1]),array.shape)).T
	points= np.column_stack((indices,array[indices[:,0],indices[:,1]]))
	
	
	triangles=np.sort(delaunay(indices).simplices)
	print("Processed image being saved as ", name)
	
	#TODO: set thse numbers to some file where they can be edited easier
	points*=[0.1,0.1,1]
	points-=np.array([ (singleton.border[1]+20)/2,(singleton.border[0]+20)/2,0])
	points=points.tolist()
	
	import pickle
	with open(path+"/temp/"+name[0:-4]+"_"+str(singleton.border[0])+"_"+str(singleton.border[1]),"wb") as f:
		f.write(pickle.dumps([points,triangles.tolist()]))
	
	return 0
