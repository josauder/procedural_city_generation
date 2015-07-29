from __future__ import division
import numpy as np
import os
import matplotlib.pyplot as plt
import procedural_city_generation

def diffusion(arr, d):
	contrib = (arr * d)
	w = contrib / 8.0
	r = arr - contrib
	N = np.roll(w, shift=-1, axis=0)
	S = np.roll(w, shift=1, axis=0)
	E = np.roll(w, shift=1, axis=1)
	W = np.roll(w, shift=-1, axis=1)
	NW = np.roll(N, shift=-1, axis=1)
	NE = np.roll(N, shift=1, axis=1)
	SW = np.roll(S, shift=-1, axis=1)
	SE = np.roll(S, shift=1, axis=1)
	diffused = r + N + S + E + W + NW + NE + SW + SE
	return diffused


def setupimage():
	
	import matplotlib.image as mpimg
	
	path=os.path.dirname(procedural_city_generation.__file__)
	#TODO: make diffused an option
	img= mpimg.imread(path+"/temp/diffused.png")
	
	for i in range(100):
		img= diffusion(img, 1)
	
	img=img**2
	return img
	

img=setupimage()


def getBuildingHeight(polygon,rahmen):
	#TODO: Export numbers to some sort of constant-singleton
	center=sum(polygon)/len(polygon)
	
	x = (center[0]+rahmen[0])/(rahmen[0]*2)
	y = (center[1]+rahmen[1])/(rahmen[1]*2)
	
	height= img[img.shape[0]-y*img.shape[0]][x*img.shape[1]][0]
	if height<0.4:
		height=min(0.035+np.random.uniform(0,1)*np.random.uniform(0,height-0.1),0.6)
	elif 0.4<height:
		if height>0.70 and np.random.uniform(0,1)<0.2:
			height*=np.random.uniform(1.3,2.6)
		else:
			height=min(0.15+np.random.uniform(0,1)*np.random.uniform(0,height-0.2),0.6)
	return height 
