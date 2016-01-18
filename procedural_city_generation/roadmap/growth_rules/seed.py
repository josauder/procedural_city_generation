from __future__ import division
import numpy as np
import random

from procedural_city_generation.roadmap.Vertex import Vertex
from procedural_city_generation.additional_stuff.rotate import rotate

from procedural_city_generation.additional_stuff.Singleton import Singleton
singleton=Singleton("roadmap")

def seed(vertex, b):

    pSeed=singleton.pSeed
    lMin=singleton.seedlMin
    lMax=singleton.seedlMax

    suggested_vertices=[]

    l=len(vertex.neighbours)
    v1=rotate(90, vertex.neighbours[0].coords-vertex.coords)
    v2=None
    if l==1:
        v2=v1
    elif l==2:
        v2=rotate(90, vertex.neighbours[1].coords-vertex.coords)*-1
    else:
        return []
    v1=v1/np.linalg.norm(v1)
    v2=v2/np.linalg.norm(v2)
    #Rechts
    if b*b*pSeed>np.random.randint(0, 100):
        l=np.random.uniform(lMin, lMax)
        k=np.random.uniform(0, 1)
        coords=((1-k)*v1+k*v2)*l
        k=Vertex(vertex.coords+coords)
        k.minor_road=True
        suggested_vertices.append(k)


    v1=v1*-1
    v2=v2*-1

    #Links
    if     b*b*pSeed>np.random.randint(0, 100):
        l=np.random.uniform(lMin, lMax)
        k=np.random.uniform(0, 1)
        coords=((1-k)*v1+k*v2)*l
        k=Vertex(vertex.coords+coords)
        k.minor_road=True
        suggested_vertices.append(k)

    return suggested_vertices
