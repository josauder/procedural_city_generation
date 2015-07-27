from __future__ import division
import numpy as np
import numpy.linalg as la
n_str_faktor = 0.08
h_str_faktor = 0.16

def weg_von_der_strasse(wedges, vertex_list, normal = True):
	global n_str_faktor, h_str_faktor
	ecken = []
	for wedge in wedges:
		a,b,c = vertex_list[wedge.a],vertex_list[wedge.b],vertex_list[wedge.c]
		v1 = a.coords - b.coords
		v2 = c.coords - b.coords
		l1 = la.norm(v1)
		l2 = la.norm(v2)
		if normal and l1 < 2*h_str_faktor or l2 < 2*h_str_faktor:
			return False
		if np.any(v1) and np.any(v2):
			n1 = np.array((-v1[1],v1[0]))/l1
			n2 = np.array((v2[1],-v2[0]))/l2
			if b.minor_road or a.minor_road:
				n1 *= n_str_faktor
			else:
				n1 *= h_str_faktor
			if b.minor_road or c.minor_road:
				n2 *= n_str_faktor
			else:
				n2 *= h_str_faktor
			if not 0 - 0.001 < wedge.alpha < 0 + 0.001:
				solution = [0,0]
				try:
					solution = la.solve(np.array(((v1),(-v2))).T,(b.coords+n2)-(b.coords+n1))
				except:
					pass
				ecken.append(b.coords + n1 + solution[0]*v1)
			else:
				ecken.append(b.coords + n1)
				ecken.append(b.coords + n2)
	return ecken
