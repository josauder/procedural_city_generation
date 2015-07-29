
import math
import numpy as np
from math import sin, cos, pi

def baumstamm(radius, texture, koords, height):
	L=[]
	for x in range(12):
		x/6.*pi
		verts=[np.array([sin(x/6.*pi), cos(x/6.*pi), 0]), np.array([sin((x+1)/6.*pi),
		cos((x+1)/6.*pi), 0]), np.array([sin((x+1)/6.*pi), cos((x+1)/6.*pi), height]),
		np.array([sin((x)/6.*pi), cos((x)/6.*pi), height]), np.array([sin((x)/6.*pi), cos((x)/6.*pi), 0])]
		verts= list(np.array(verts)+koords)
		faces=range(len(verts))
		L.append(Polygon(verts, faces, texture))
	return L
	

r=1
texture="braun"
koords=np.array([10,0,0])
height=15
print baumstamm(r, texture, koords, height)
