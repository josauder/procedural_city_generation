import numpy as np
import numpy.linalg as la
import matplotlib.pyplot as plt
from copy import copy
from weg_von_der_strasse import weg_von_der_strasse
class Kante(object):
	def __init__ (self, e1, e2, strasse=True):
		self.e1, self.e2 = e1, e2
		self.v = e2 - e1
		self.l = la.norm(self.v)
		self.n = np.array(((self.v/self.l)[1],-(self.v/self.l)[0]))
		self.strasse = strasse
		
	def __str__(self):
		return str(self.e1) + str(self.e2)
		
	def __repr__(self):
		return "Kante: " + str(self)
		
	def selfplot(self, c = "k"):
		plt.plot((self.e1[0],self.e2[0]),(self.e1[1],self.e2[1]), c)
		
class Poly(object):
	def __init__(self, kanten):
		self.kanten = [k for k in kanten if np.any(k.e1-k.e2)]
		self.punkte= [np.array([x.e1[0],x.e1[1],0]) for x in self.kanten]
		for kante in self.kanten:
			if kante.strasse:
				self.strasse = True
				break
		else:
			self.strasse = False
			
	def flaeche(self):
		p = [k.e1 for k in self.kanten]
		return 0.5 * abs(sum(x0*y1 - x1*y0 for ((x0, y0), (x1, y1)) in zip(p, p[1:] + [p[0]])))
			
	def laengste_kante(self):
		return self.kanten[np.argmax([kante.l for kante in self.kanten])]
		
	#def is_convex(self):
	#	for (k1,k2) in zip(self.kanten, self.kanten[1:]+[self.kanten[0]]):
	#		v = k2.v-k1.v
	#		alpha = np.arctan2(v[1],v[0])
	#		if alpha
		
	def teilen(self):
		global min_flaeche,grndstck_breite

		if self.flaeche() > min_flaeche:
			k = self.laengste_kante()
			p = k.e1 + k.v/(np.random.uniform(0.95,1.05)*2)
			alt_kanten = self.kanten
			neu_ecken = []
			schalter = True
			for kante in self.kanten:
				wird_geschnitten = False
				try:
					x = np.linalg.solve(np.array([k.n,-kante.v]).T,kante.e1-p)
					if 0.0001 < x[1] < 0.99999:
						schnittpunkt = p + x[0]*k.n
						wird_geschnitten = True
				except:
					pass
				if wird_geschnitten:
					neu_ecken.append((schnittpunkt, schalter))
					schalter = not schalter
					neu_ecken.append((schnittpunkt, schalter))
				else:
					neu_ecken.append((kante.e1, schalter))
					neu_ecken.append((kante.e2, schalter))
					
			a_ecken = [x[0] for x in neu_ecken if x[1]]
			b_ecken = [x[0] for x in neu_ecken if not x[1]]
			a_kanten = [Kante(e1,e2) for (e1,e2) in zip(a_ecken, a_ecken[1:]+[a_ecken[0]])]
			b_kanten = [Kante(e1,e2) for (e1,e2) in zip(b_ecken, b_ecken[1:]+[b_ecken[0]])]
			for kante in a_kanten+b_kanten:
				for alt in alt_kanten:
					if (not np.any(kante.e1 - alt.e1)) or (not np.any(kante.e2 - alt.e2)):
						kante.strasse = alt.strasse
						break
				else:
					kante.strasse = False
			A = Poly(a_kanten)
			B = Poly(b_kanten)
			if A.strasse and B.strasse:
				return [A,B]
			return False
		return False
		
	def __repr__(self):
		return "Polygon:" + str(self.kanten)
		
	def selfplot(self):
		colors = "bgrcmyk"
		i = np.random.randint(len(colors))
		for kante in self.kanten:
			kante.selfplot(colors[i])

#####Aufteilen mit Petrasch-Algorithmus#######

min_flaeche = 0.2

	
def aufteilen(poly):
	zu_teilen = [poly]
	naechste = []
	fertig = []
	while zu_teilen:
		for x in zu_teilen:
			geteilt = x.teilen()
			if geteilt:
				naechste += geteilt
			else:
				fertig.append(x)
		zu_teilen,naechste = naechste, []
	return fertig	
	
def grundstuecke(polylist, vertex_list):
	grosseflaechen=[]
	grundstuecke = []
	for p in polylist:
		ecken = weg_von_der_strasse(p, vertex_list)
		if ecken:
			kanten = [Kante(e1,e2) for (e1,e2) in zip(ecken, ecken[1:]+[ecken[0]])]
			poly = Poly(kanten)
			if len(p) < 20:
				for grundstueck in aufteilen(poly):
					grundstuecke.append(grundstueck)
			else:
				grosseflaechen.append(poly)			
	return grundstuecke,grosseflaechen
	
def main(polygon_list,vertex_list):
	lots,grosseflaechen = grundstuecke(polygon_list, vertex_list)
	strassen = max(polygon_list, key = lambda x: len(x))
	ecken = weg_von_der_strasse(strassen, vertex_list, normal=False)
	kanten = [Kante(e1,e2) for (e1,e2) in zip(ecken, ecken[1:]+[ecken[0]])]
	strassen_poly = Poly(kanten)
	if len(grosseflaechen)>0:
		grosseflaechen.remove(max(grosseflaechen, key= lambda x: len(x.punkte)))
	return lots,grosseflaechen, strassen_poly
	
	
	
	
if __name__=="__main__":
	import konstruieren
	polygon_list,vertex_list = konstruieren.main()	
	main(polygon_list,vertex_list)
	grundstuecke,strassen_poly = main()
	print "Anzeigen..."
	fig = plt.figure()

	strassen_poly.selfplot()

	fig2 = plt.figure()
	for g in grundstuecke:	
		g.selfplot()
	plt.show()
					
			
				
				
				
		
	
