# -*- coding: utf-8 -*-
from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as la
from Poly import Poly
from weg_von_der_strasse import weg_von_der_strasse, h_str_faktor, n_str_faktor
from aufteilen import aufteilen

def kuerzeste_seite(p, knotenliste):
	s = np.inf
	p = [knotenliste[wedge.b].koords for wedge in p]
	for (k1, k2) in zip(p, p[1:]+[p[0]]):
		l = la.norm(k2 - k1)
		if l < s:
			s = l
	return s
	
			
def grundstuecke(polygonliste,knotenliste):
	global min_flaeche
	lots = []
	for x in polygonliste:
		if kuerzeste_seite(x, knotenliste) > 2*h_str_faktor:
			ecken = weg_von_der_strasse(x,knotenliste)
			poly = Poly(ecken)	
			lots.append(poly)
		else:
			print "Zu klein!"
	return lots

		
if __name__=="__main__":
	import konstruieren
	polygone,knotenliste=konstruieren.main()
	fig=plt.figure()
	polygone = polygone[:2]
	
	grundstuecke = [aufteilen(x) for x in grundstuecke(polygone,knotenliste)]
	for geteilt in grundstuecke:
		for lot in geteilt:
			for (p1,p2) in zip(lot, lot[1:]+(lot[0])):
				plt.plot((p1[0],p2[0]),(p1[1],p2[1]))
	
	plt.show()


