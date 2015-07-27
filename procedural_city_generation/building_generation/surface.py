import numpy as np
import procedural_city_generation
import os

path=os.path.dirname(procedural_city_generation.__file__)

with open(path+"/temp/heightmap_in_use.txt", "r") as f:
	inuse=f.read()

with open(path+"/inputs/heightmaps/"+inuse) as f:
	surfacetext=f.read()
	
surface=surfacetext.split("_\n")
surface=surface[0]

surface=[x for x in surface.split("\n") if x is not '']
surface3D=[]
surface2D=[]
for line in surface:
	words=[float(x) for x in line.split(" ") if x is not '']
	surface3D.append(np.array(words))
	surface2D.append(np.array(words[0:2]))
surface2D=np.array(surface2D)
surface3D=np.array(surface3D)

from scipy.spatial import cKDTree
tree=cKDTree(surface2D, leafsize=160)



def getSurfaceHeight(coords):
	results=[]
	for c in coords:
		res=tree.query(np.array(c[0:2]),3)
		results.extend(res[1])
	h=0
	l=len(results)
	r=[surface3D[results[i]][2]+0.03 for i in range(len(results))]
	return min(r),max(r)
	
