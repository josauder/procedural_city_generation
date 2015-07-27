import numpy as np
def find_radial_centers(variables):
	'''Intended to find areas where the rule-image is blue and return the center of such areas'''
	img=variables.img
	Aufloesung=variables.bildaufloesung
	quadrate=[]
	for x1 in range( np.shape(img)[0] //Aufloesung ):
		for x2 in range( np.shape(img)[1]//Aufloesung):
			quadrate.append([x1,x2])
			
	quadrate= [q for q in quadrate if np.argmax(img[q[0]*Aufloesung][q[1]*Aufloesung])==2] #auf blaue reduzieren
	
	flaechen=[]

	while len(quadrate)>0:   #Flaechen finden, also Quadrate auf Flaechen aufteilen      
		flaechen.append([quadrate[0]])
		quadrate.pop(0)
		h=0
		while h<len( flaechen[len(flaechen)-1] ):
			q=flaechen[len(flaechen)-1][h]
			for nachbar in[[q[0]-1,q[1]], [q[0]+1,q[1]], [q[0],q[1]-1],[q[0],q[1]+1]]:
				if nachbar in quadrate:
					flaechen[len(flaechen)-1].append(nachbar)
					quadrate.remove(nachbar)
			h+=1

	zentren=   [ np.array([sum( [x[0] for x in y])/len(y)*Aufloesung, sum([x[1] for x in y])/len(y)*Aufloesung]) for y in flaechen]
	return zentren
