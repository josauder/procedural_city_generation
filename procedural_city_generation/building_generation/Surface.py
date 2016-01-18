import numpy as np
import procedural_city_generation
import os


class Surface(object):
    def __init__(self, input_name):
        print("Surface is being set up for getting of getSurfaceHeight")
        path=os.path.dirname(procedural_city_generation.__file__)

        with open(path+"/temp/"+input_name+"_heightmap.txt", 'r') as f:
            inuse=f.read()

        import pickle
        with open(path+"/temp/"+inuse, 'rb') as f:
            self.surface3D, triangles=pickle.loads(f.read())
        self.surface2D=np.array(self.surface3D)[::, :2]

        from scipy.spatial import cKDTree
        self.tree=cKDTree(self.surface2D, leafsize=160)
        print("Setup of surface finished")


    def getSurfaceHeight(self, coords):
        results=[]
        for c in coords:
            res=self.tree.query(np.array(c[0:2]), 3)
            results.extend(res[1])
        h=0
        l=len(results)
        r=[self.surface3D[results[i]][2]+0.03 for i in range(len(results))]
        return min(r), max(r)

