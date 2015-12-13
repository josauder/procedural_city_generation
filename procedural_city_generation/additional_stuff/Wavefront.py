__author__ = 'jonathan'
import procedural_city_generation
import os, sys

class Wavefront(object):

    def __init__(self,textures,polygon3ds,outpath="/outputs/"):
        self.textures=textures
        self.polygon3ds=polygon3ds
        self.outpath=os.path.dirname(procedural_city_generation.__file__)+outpath
        self.writeMtllib()

        self.n_vertices=1

        self.writeObj()

    def writeMtllib(self):
        mtllib=""
        for tex in self.textures:
            mtllib+="newmtl "+ tex + "Ka 1 1 1\nKd 1.0 1.0 1.0\nKs 0 0 0\nmap_Ka "+tex+"\nmap_Kd "+tex +"\n"
        with open(self.outpath+"out.mtl", 'w' ) as f:
            f.write(mtllib)
        return 0

    def writeObj(self):
        out="mtllib out.mtl\nvt 0 0 0\nvt 0 1 0\nvt 1 1 0\nvt 1 0 0\n"


        g=lambda f: "f "+"".join([str(f[a])+"/"+str(a)+" " for a in range(len(f))])+"\n"




        for n,polygon in enumerate(self.polygon3ds):


            out+="o object"+str(n)\
                 +"\nusemtl "+\
                 polygon.texture+"\n"+\
                 ("".join(["v " +" ".join(map(str,vert))+"\n" for vert in polygon.verts]))+\
                 ("".join([g(np.array(face)+self.n_vertices) for face in polygon.faces]))

            self.n_vertices+=len(polygon.verts)

        with open(self.outpath+"out.obj",'w') as f:
            f.write(out)
        return 0

if __name__ == '__main__':
    import procedural_city_generation
    from procedural_city_generation.building_generation.Polygon3D import Polygon3D
    import numpy as np

    testPoly=Polygon3D([np.array([0,0,0]),np.array([0,1,0]),np.array([1,1,0]),np.array([1,0,0])],[range(4)],"Floor02.jpg")
    Wavefront(["Floor02.jpg"],[testPoly])