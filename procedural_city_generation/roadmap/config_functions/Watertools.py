import numpy as np

class Watertools:
	def __init__(self, heightmap):
		self.heightmap=heightmap
		self.new=None
		self.old=self.heightmap
		self.flooded=np.zeros(self.heightmap.shape)
		
		
		
		
			
			
			
			
	
	def flood(self, h, pos):
		"""
		pos is a pair of indices on heightmap (position where it gets flooded)
		h is the corresponding height
		"""
		
		flooded=np.zeros(self.heightmap.shape)
		
		stencil=np.array([
		[-1,0],
		[1,0],
		[0,1],
		[0,-1]
		])
	
		front=[pos]
		while len(front)>0:
			new_front=[]
			for x in front:
				if self.old[x[0]][x[1]]<h:
					flooded[x[0]][x[1]]=1
					new_front.extend(
					[new for new in x+stencil if not flooded[new[0]][new[1]] and not np.any(x<=0) and not x[0]>=flooded.shape[0]-2 and not x[1]>=flooded.shape[1]-2]
					)
					
			front=new_front
			
		self.new=self.old
		self.new[np.argwhere(flooded)]=h
		self.flooded[np.argwhere(flooded)]=1
		return flooded
		
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
			front=[np.argwhere(heightmap!=-np.inf)[0]]
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
	Watertools()
