import numpy as np
import procedural_city_generation
import os

print "Surface is being set up for getting of getSurfaceHeight"
path=os.path.dirname(procedural_city_generation.__file__)

with open(path+"/temp/heightmap_in_use.txt", "r") as f:
	inuse=f.read()

import pickle
with open(path+"/temp/"+inuse) as f:
	surface3D, triangles=pickle.loads(f.read())

surface2D=np.array(surface3D)[::,:2]

from scipy.spatial import cKDTree
tree=cKDTree(surface2D, leafsize=160)
print "Setup of surface finished"


def getSurfaceHeight(coords):
	results=[]
	for c in coords:
		res=tree.query(np.array(c[0:2]),3)
		results.extend(res[1])
	h=0
	l=len(results)
	r=[surface3D[results[i]][2]+0.03 for i in range(len(results))]
	return min(r),max(r)
	
