import numpy as np

def rotate(angle,vector):
	'''rotates a 2D Vector by an angle in the mathematically-positive direction
	where:
	   angle=angle
	   vector=vector
	'''
	if angle==90:
		return np.array([-vector[1],vector[0]])
		
	angle=angle*np.pi/180
	matrix=np.array([np.cos(angle),
	np.sin(angle),
	-np.sin(angle),
	np.cos(angle)])
	
	
	matrix=matrix.reshape(2,2)
	matrix=np.dot(vector,matrix)

	return matrix
