def find_land_bodies(heightmap, h):
	"""
	This function finds out if the land that is not covered by water is connected, and if not, then finds all bodies 
	
	Parameters
	-----------
	- heightmap : np.ndarray(h,w) heightmap image
	- h : Height of water
	
	Returns
	----------
	- list<list<np.ndarray>> : list of land-bodies, which are a list containing numpy.ndarray(2,)'s. If list is empty, there is no water or all is water.
	
	"""
	
	underwater_arr=np.argwhere(arr<h)
	heightmap[underwater_arr]=-np.inf
	dims=(heightmap.shape[0]*heightmap.shape[1])
	total=dims-len(underwater_arr)
	if total==0:
		print "ERROR: seperate_water.py \n The entire map is under the water level"
		return []
	elif total==0:
		print "There is no water on this map"
		return []
	
	stencil=np.array([[0,1],[0,-1],[1,0],[-1,0]])
	
	done=np.zeros(heightmap.shape)
	
	bodies=0
	body_list=[]
	while total>0:
		bodies+=1
		body=[]
		front=[np.argwhere(heightmap not -np.inf)[0]]
		while len(front)>0:
			for x in front:
				if x[0]>=0 and x[1]>=0 and x[0]<heightmap.shape[0] and x[1]<heightmap.shape[1]:
					new=[g for g in [ el for el in np.array([x,x,x,x])-stencil] if done[g]==0]
					g[new]=1
					neufront.extend(new)
			front=neufront
			body.extend(front)
		body_list.append(body)
	return bodies



if __name__ == '__main__':
	main()
