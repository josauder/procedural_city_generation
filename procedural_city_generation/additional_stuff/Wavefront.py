__author__ = 'jonathan'
import procedural_city_generation
import os, sys
import numpy as np
path=os.path.dirname(procedural_city_generation.__file__)
class Wavefront(object):

    def __init__(self, textures, polygon3ds, outpath="/outputs/"):
        self.textures=textures
        self.polygon3ds=polygon3ds
        self.outpath=os.path.dirname(procedural_city_generation.__file__)+outpath
        self.writeMtllib()

        self.n_vertices=1

        self.writeObj()

    def writeMtllib(self):
        mtllib=""
        for tex in self.textures:
            mtllib+="newmtl "+ tex + "\nKa 1 1 1\nKd 1.0 1.0 1.0\nKs 0 0 0\nmap_Ka "+path+"/visualization/Textures/"+tex+"\nmap_Kd "+path+"/visualization/Textures/"+tex +"\n"
        with open(self.outpath+"out.mtl", 'w' ) as f:
            f.write(mtllib)
        return 0

    def writeObj(self):
        out="mtllib "+path+"/outputs/out.mtl\nvt 0 0 0\nvt 0 1 0\nvt 1 1 0\nvt 1 0 0\n"
        g=lambda f: "f "+"".join([str(f[a])+"/"+str(a+1)+" " for a in range(len(f))])+"\n"

        for n, polygon in enumerate(self.polygon3ds):


            out+="o object"+str(n)\
                 +"\nusemtl "+\
                 polygon.texture.name+"\n"+\
                 ("".join(["v " +" ".join(map(str, vert))+"\n" for vert in polygon.verts]))+\
                 ("".join([g(np.array(face[:4])+self.n_vertices) for face in polygon.faces]))
            # when fixed, replace with line below
#                 ("".join([g(np.array(face)+self.n_vertices) for face in polygon.faces]))

            self.n_vertices+=len(polygon.verts)

        with open(self.outpath+"out.obj", 'w') as f:
            f.write(out)
        return 0

if __name__ == '__main__':
    import procedural_city_generation
    from procedural_city_generation.building_generation.Polygon3D import Polygon3D
    import numpy as np

#    testPolys=[Polygon3D([np.array([0, 0, 0]), np.array([0, 1, 0]), np.array([1, 1, 0]), np.array([1, 0, 0])], [range(4)], "Floor02.jpg"),
#    Polygon3D(np.array([1, 1, 1])+np.array([np.array([0, 0, 0]), np.array([0, 1, 0]), np.array([1, 1, 0]), np.array([1, 0, 0])]), [range(4)], "Floor01.jpeg"),
#    Polygon3D(np.array([2, 2, 2])+np.array([np.array([0, 0, 0]), np.array([0, 1, 0]), np.array([1, 1, 0]), np.array([1, 0, 0])]), [range(4)], "Floor04.jpeg")]
#    Wavefront(["Floor02.jpg", "Floor01.jpeg", "Floor04.jpeg"], testPolys)