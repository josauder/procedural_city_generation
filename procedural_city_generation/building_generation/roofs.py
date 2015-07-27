# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
from cuts import scale, scaletransform_vertex


import random
#class Kante(object):
#	def __init__(self, p1, p2):
#		self.p1=p1
#		self.p2=p2
#		self.laenge= abs(p1-p2)
def roof(walls,roofwalls,haus,height):
	h=np.random.uniform(0.04,0.08)
	coords=[]
	for wall in roofwalls:
		for i in range(len(wall)-1):
			coords.append(wall[i]+np.array([0,0,height]))
			
			
	kanten=[[coords[i-1],coords[i]] for i in range(len(coords))]

	if haus and len(coords)==4:
		return hausroof(kanten,h)
	else:
		return kastenroof(roofwalls,kanten,coords,height,height+h)





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


def hausroof(kanten, h):
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
	return [[x[0] for x in f1],[x[0] for x in f2],[x[0] for x in f3], [x[0] for x in f4]]
		

def kastenroof(walls,kanten,coords,height,h):
	
	from buildinggenerator import buildwalls,flatebene
	kasten=scaletransform_vertex(coords,np.random.uniform(0.5,0.15),sum(coords)/len(coords),random.randint(0,2))
	for k in kasten:
		if not pinpoly(kanten,k):
			return [flatebene(walls,height)]
			
	r=buildwalls([[kasten[i-1],kasten[i]] for i in range(len(kasten))],height,h)
	r.append([x+np.array([0,0,h-height]) for x in kasten])
	
	r.append(flatebene(walls,height))
	return r

#def kasten(Liste, Hoehe):
#	Flaechen=[]
#	Flaechen.append([Kante(x.p1+np.array([0,0,Höhe]), x.p2+np.array([0,0,Hoehe])) for x in Liste])
#	for kante in Liste:
#		Flaechen.append( [kante, Kante(kante.p2, kante.p2+np.array([0,0,Hoehe])),
#		Kante(kante.p2+np.array([0,0,Hoehe]), kante.p1+np.array([0,0,Hoehe])),
#		Kante(kante.p1+np.array([0,0,Hoehe]), kante.p1)])
#	return Flaechen
#p1= np.array([0,0,0])
#p2= np.array([1,0,0])
#p3= np.array([1,1,0])
#p4= np.array([0,1,0])


#test=[ [p1,p2], [p2,p3], [p3,p4], [p4,p1] ]
#print roof1(test, 5.2)
