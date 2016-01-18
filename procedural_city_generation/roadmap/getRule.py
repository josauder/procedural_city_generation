# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
from procedural_city_generation.additional_stuff.Singleton import Singleton

singleton=Singleton("roadmap")

def getRule(vertex):
    """
    Gets the correct growth_rule for a Vertex, depending on that objects'
    xy coordinates and the growth_rule_image

    Parameters
    ----------
    vertex : Vertex object

    Returns
    -------
    tuple(int, np.ndarray(3, ) , float)
        (int) for choosing the correct growth rule,
        (np.ndarray) for center in case that the radial rule is chosen,
        (float) for population_density
    """
    x = (vertex.coords[0]+singleton.border[0])/(singleton.border[0]*2)
    y = (vertex.coords[1]+singleton.border[1])/(singleton.border[1]*2)

    population_density = np.sqrt((singleton.img2[singleton.img2.shape[0]-y*singleton.img2.shape[0]][x*singleton.img2.shape[1]][0])/255)
    if vertex.seed:
        return (4, None, population_density)


    if not vertex.minor_road:
        #Finds the relative position of the vertex on the growth_rule_image
        intrule=np.argmax(singleton.img[singleton.img.shape[0]-y*singleton.img.shape[0]][x*singleton.img.shape[1]])
        z=(0, 0)

        #If the rule is radial, find the closest radial center
        if intrule == 2:
            z=singleton.center[np.argmin(np.linalg.norm(vertex.coords-singleton.center, axis=1))]
        return (intrule, z, population_density)
    else:
        return (3, None, population_density)
