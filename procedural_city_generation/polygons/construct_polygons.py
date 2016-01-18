from __future__ import division

import numpy as np
import math
import matplotlib
import matplotlib.pyplot as plt



class Wedge(object):
    def __init__(self, a, b, c, alpha):
        self.a=a
        self.b=b
        self.c=c
        self.alpha=alpha
    def __repr__(self):
        return "W["+str(self.a)+", \t"+str(self.b)+", \t"+str(self.c)+"]"

def getWedges(vertex_list):
    '''Constructs all inner Angles as Wedges of the Vertices A-B-C so that there exists exactly one Wedge B-C-X1.'''
    from operator import itemgetter, attrgetter
    allWedges=[]

    for vertex in vertex_list:
        orderedconnections=[]
        number_of_neighbours=0
        for neighbour in vertex.neighbours:

            alpha=np.arctan2(neighbour.coords[1]-vertex.coords[1], neighbour.coords[0]-vertex.coords[0])
            if alpha<0:
                alpha+=2*np.pi
            orderedconnections.append([ neighbour.selfindex, alpha])
            number_of_neighbours+=1


        orderedconnections.sort(key=itemgetter(1))


        for i in range(number_of_neighbours):
            this=orderedconnections[i-1]
            afterthis=orderedconnections[i]
            if i == 0:
                winkel = this[1] - afterthis[1] + 2*np.pi
            else:
                winkel = afterthis[1]-this[1]
            winkel %= 2*np.pi
            neueswedge=Wedge(this[0], vertex.selfindex, afterthis[0], winkel)
            allWedges.append(neueswedge)

    allWedges.sort(key=attrgetter('a', 'b'))
    return allWedges



def getPolygon2Ds(vertex_list):
    '''Finds all closed Polygon2Ds. The algorithm starts with Wedge A-B-C and looks for Wedge B-C-X1, C-X1-X2... A polygon is found when Xn==A'''
    wedgeliste=getWedges(vertex_list)

    from bisect import bisect_left as search
    allpolygons=[]

    def search(x):
        s1=x.b
        s2=x.c
        for wedge in wedgeliste:
            if wedge.a==s1 and wedge.b==s2:
                return wedge

    while len(wedgeliste)>0:
        start=x=wedgeliste[0]
        currentpolygon=[]
        while True:
            if not (np.pi - 0.001 < x.alpha < np.pi + 0.001) :
                currentpolygon.append(x)
            x=search(x)
            if x is not None:
                wedgeliste.remove(x)
                if x is start:

                    allpolygons.append(currentpolygon)
                    break
    return allpolygons



def main(vertex_list=None):
    '''Input: list of vertices representing the Roadmap
    Output: List of all Polygon2Ds representing Lots,
    List of all Polygon2Ds representing Blocks
    List of all Polygon2Ds which are too large to be Lots
    Polygon2D representing the road-network'''
    import sys
    sys.path.append('/home/lenny/Documents/Stadtprojekt/procedural_city_generation')
    if vertex_list is None:
        from procedural_city_generation.additional_stuff import pickletools

        vertex_list=pickletools.reconstruct()
        print("Reconstructing of data structure finished")

    import os
    import procedural_city_generation
    path=os.path.dirname(procedural_city_generation.__file__)

    with open(path+"/temp/border.txt", "r") as f:
        border=f.read()
    border=[int(x) for x in border.split(" ") if x is not '']

    print("Extracting Polygon2Ds")
    from procedural_city_generation.polygons import construct_polygons
    polylist=construct_polygons.getPolygon2Ds(vertex_list)
    print("Polygon2Ds extracted")
    return polylist, vertex_list

if __name__ =='__main__':
    main()






