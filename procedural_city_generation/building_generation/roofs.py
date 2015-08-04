# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt

from procedural_city_generation.building_generation.cuts import *
from procedural_city_generation.building_generation.building_tools import *
from procedural_city_generation.building_generation.Polygon3D import Polygon3D
from procedural_city_generation.additional_stuff.Singleton import Singleton
singleton=Singleton("building_generation")

def roof(walls,roofwalls,height,housebool,texture1,texture2=None):
	
	#TODO: add to some kind of config object
	h=np.random.uniform(singleton.roofheight_min,singleton.roofheight_max)
	
	coords=[]
	for wall in roofwalls:
		for i in range(len(wall)-1):
			coords.append(wall[i]+np.array([0,0,height]))
			
			
	kanten=[[coords[i-1],coords[i]] for i in range(len(coords))]

	if len(coords)==4 and housebool:
		return hausroof(kanten,h,texture1)
	else:
		return kastenroof(walls,roofwalls,kanten,coords,height,height+h,texture1,texture2)

def isleft(kante,point):
	return ((kante[1][0]-kante[0][0])*(point[1]-kante[0][1]) - (point[0]-kante[0][0]) * (kante[1][1]-kante[0][1]))
	
def pinpoly(kanten,point):
	counter=0
	
	for kante in kanten:
		if kante[0][1] <= point[1]:
			if kante[1][1] > point[1]:
				if isleft(kante,point) >0:
					counter+=1
			elif kante[1][1] <= point[1]:
				if isleft(kante,point) <0:
					counter-=1
	if counter!=0:
		return True
	return False


def hausroof(kanten, h, texture):
	if np.linalg.norm(kanten[0][1]-kanten[0][0])<np.linalg.norm(kanten[1][1]-kanten[1][0]):
	#kanten[0].laenge<kanten[1].laenge:
		p1=(kanten[0][1]+kanten[0][0])/2+np.array([0,0,h])
		p2=(kanten[2][1]+kanten[2][0])/2+np.array([0,0,h])
		f1=[kanten[0], [kanten[0][1], p1], [p1, kanten[0][0]]]
		f2=[kanten[2], [kanten[2][1], p2], [p2, kanten[2][0]]]
		f3=[kanten[1], [kanten[1][1], p2], [p2, p1], [p1, kanten[1][0]]]
		f4=[kanten[3], [kanten[3][1], p1], [p1, p2], [p2, kanten[3][0]]]
	else:
		p1=(kanten[1][1]+kanten[1][0])/2+np.array([0,0,h])
		p2=(kanten[3][1]+kanten[3][0])/2+np.array([0,0,h])
		f3=[kanten[0], [kanten[0][1], p1], [p1,p2], [p2, kanten[0][0]]]
		f4=[kanten[2], [kanten[2][1], p2], [p2,p1], [p1, kanten[2][0]]]	
		f1=[kanten[1], [kanten[1][1], p1], [p1, kanten[1][0]]]
		f2=[kanten[3], [kanten[3][1], p2], [p2, kanten[1][0]]]
	l=[[x[0] for x in f1],[x[0] for x in f2],[x[0] for x in f3], [x[0] for x in f4]]
	return [Polygon3D(x,range(len(x)),texture) for x in l]

def kastenroof(walls,roofwalls,kanten,coords,height,h,texture1,texture2=None):
	if texture2 is None:
		texture2=texture1
		
		
	kasten=scaletransform_vertex(coords,np.random.uniform(0.5,0.15),sum(coords)/len(coords),random.randint(0,2))
	for k in kasten:
		if not pinpoly(kanten,k):
			return [flatebene(walls,height,texture1)]
	r=buildwalls([[kasten[i-1],kasten[i]] for i in range(len(kasten))],height,h,texture2)
	r.append(Polygon3D([x+np.array([0,0,h-height]) for x in kasten],range(len(kasten)),texture2))
	
	r.append(flatebene(walls,height,texture1))
	return r


