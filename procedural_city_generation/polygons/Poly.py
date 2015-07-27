# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt



class Ecke(object):
	def __init__(self,tupel):
		(self.a,self.b,self.c,self.alpha) = tupel
		self.v1 = self.a - self.b
		self.n1 = np.array((-self.v1[1],self.v1[0]))/la.norm(self.v1)
		self.v2 = self.c - self.b
		self.n2 = np.array((self.v2[1],-self.v2[0]))/la.norm(self.v2)
		self.mv = (self.n1 + self.n2) / (la.norm(self.n1 + self.n2) * np.sin(self.alpha/2))
	
	def __repr__(self):
		return "Ecke:/nXY: %s, V1: %s, MV: %s, V2: %s, Winkel: %s" %(self.b, self.v1, self.mv, self.v2, self.alpha)
		
	def selfplot(self):
		plt.plot(((self.mv + self.b)[0], self.b[0]), ((self.mv + self.b)[1], self.b[1]))
		
class Poly(object):
	def __init__(self,ecken):
		self.ecken = [Ecke(tupel) for tupel in ecken]
		self.kanten = zip(self.ecken,self.ecken[1:]+[self.ecken[0]])
		self.points= [x.b for x in self.ecken]
		
	
	def __repr__(self):
		return str(self.ecken)
	
	def selfplot(self):
		for (e1,e2) in self.kanten:
			plt.plot((e1.b[0],e2.b[0]),(e1.b[1],e2.b[1]),'k')

if __name__=="__main__":
	import konstruieren
	from neu_aufteilen import weg_von_der_strasse
	polygone,knotenliste=konstruieren.main()
	
	fig=plt.figure()
	poly = Poly(weg_von_der_strasse(polygone[0],knotenliste))
	poly.selfplot()
	plt.show()

			

