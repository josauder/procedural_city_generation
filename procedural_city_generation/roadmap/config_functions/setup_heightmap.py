import numpy as np
import os
def setup_heightmap(variables,path):		
	'''Sets up the heightmap image from roadmap.conf entry heightmap_name, writes ./Heightmaps/inuse.txt so other functions know which heightmap to load
	possible inputs:
	random: generates a new random map with randommap.py
	insert_name
	insert_name.png
	insert_name.txt
	'''
	
	#TODO make inputs more flexible
	name=variables.heightmap_name
	
	#if conf.txt entry is "random", then /stadt/Polygone/randommap.py will be called to create a new random map in the correct size
	if name=="random":
		print "New random heightmap is being created with randommap.py"
		#Writes correct inuse.txt
		from procedural_city_generation.additional_stuff import randommap
		randommap.main(variables.border,path)
		
		with open(path+"/temp/heightmap_in_use.txt",'w') as f:
			f.write("randommap.txt")
		return 0
	
	
	#Writes correct inuse.txt
	with open(path+"/temp/heightmap_in_use.txt",'w') as f:
		f.write(name[0:-3]+"txt")
	
	with open(path+"/temp/border.txt",'r') as f:
		dimensions=f.read()
		
		
	#If a txt has already been written for the input in the image, OR if the input was a .txt to begin with, simply load that txt
	if (name[0:-3]+"txt" in os.listdir(path+"/inputs/heightmaps/")) and (dimensions==str(variables.border[0])+" "+str(variables.border[1])):
			return 0
	
	#If the given image has no .txt yet, write the corresponding.txt
	
	#Load image and resize
	from PIL import Image
	img = Image.open(path+'/inputs/heightmaps/'+name)    
	
	
	#TODO: set these numbers to some file where they can be edited easier
	rsize = img.resize(((variablen.rahmen[1]+20)*10,(variablen.rahmen[0]+20)*10))
	array = np.asarray(rsize) 
	from copy import copy
	array=copy(array)
	
	
	#If image is a jpeg, all values have to be divided by 255
	array=array[::,:,0]/255.
	
	print "You have selected a heightmap which has no .txt file yet, OR the given .txt file has the wrong dimensions. \n Please enter the difference between max-height and min-height"
	h=float(raw_input(">>>h="))
	print "You have entered",h, "as height"
	print "Processing image"
	
	
	#TODO: Find and Fix this Bug
	array*=abs(h)
	#Caused weird bugs when -=h was used.. I still can't explain them...
	array-= h+0.01
	
	#Create all necessary stuff for the heightmap
	from scipy.spatial import Delaunay as delaunay
	indices	=	np.vstack(np.unravel_index(np.arange(array.shape[0]*array.shape[1]),array.shape)).T
	points= np.column_stack((indices,array[indices[:,0],indices[:,1]]))
	
	triangles=np.sort(delaunay(indices).simplices)
	print "Processed image being saved as ", name
	
	#Save heightmap as txt
	name=name[0:-3]+"txt"
	savestr=""
	
	
	
	#TODO: set thse numbers to some file where they can be edited easier
	for p in points:
		savestr+=str(p[0]/10-(variables.border[1]+20)/2)+" "+str(p[1]/10-(variables.border[0]+20)/2)+" "+str(p[2])+"\n"
	
	
	#TODO: Document how heightmap is being saved somewhere
	savestr+="_\n"
	
	for t in triangles:
		savestr+=str(t[0])+" "+str(t[1])+" "+str(t[2])+"\n"
	with open(path+"/inputs/heightmaps/"+name,"w") as f:
		f.write(savestr)
	return 0
