from __future__ import division
import numpy as np

def is_convex(self):
	for (edge1, edge2) in zip(self.edges, self.edges[1:] + [self.edges[0]]):
		v = edge2.dir_vector - edge1.dir_vector
		angle = np.arctan2(v[1],v[0])
		if angle >= np.pi or (angle < 0 and angle + 2*np.pi >= np.pi):
			return False
	return True
	
class Edge(object):
	
	def __init__(self, vertex1, vertex2, bordering_road = True):
		"""Input vertices are numpy-arrays"""
		self.bordering_road = bordering_road
		self.vertices = (vertex1, vertex2)
		self.dir_vector = vertex2 - vertex1
		self.length = np.linalg.norm(self.dir_vector)
		v = self.dir_vector/self.length
		self.n = np.array((v[1],-v[0]))
		
	def __getitem__(self, i):
		return self.vertices[i]
		
	def __repr__(self):
		return str([round(x, 2) for x in self[0]]) + ", " + str([round(x, 2) for x in self[1]])	
		
class Polygon(object):
	
	def __init__(self, in_list, poly_type="vacant"):
		"""Input may be numpy-arrays or Edge-objects"""

		if isinstance(in_list[0], Edge):
			self.edges = in_list
			self.vertices = [edge[0] for edge in self.edges]
		else:
			self.vertices = in_list
			self.edges = [Edge(v1,v2) for v1,v2 in 
							zip(in_list, in_list[1:]+[in_list[0]])]
		self.is_convex = is_convex(self)
		self.poly_type = poly_type
				
	def __repr__(self):
		s = "Polygon: \n"
		for vertex in self.vertices:
			s += str([round(x, 2) for x in vertex]) + "\t"
		s += "\n"
		return s
			
	def area(self):
		"""Return area of polygon"""
		return 0.5 * abs(sum(edge[0][0]*edge[1][1] - edge[1][0]*edge[0][1]
													for edge in self.edges))
			
	def is_convex(self):
		for (edge1, edge2) in zip(self.edges, self.edges[1:] + [self.edges[0]]):
			v = edge2.dir_vector - edge1.dir_vector
			angle = np.arctan2(v[1],v[0])
			if angle >= np.pi or (angle < 0 and angle + 2*np.pi >= np.pi):
				return False
		return True
				
	
	def split(self, min_area=0.6, min_length=0.2, eps=10**-5):
		return False#for testing purposes
		"""Split polygon into two parts"""
		sorted_edges = sorted(self.edges, key=lambda x: -x.length)
		split_edge = sorted_edges[0]
		i = 1
		len_edges = len(sorted_edges)
		
		while split_edge.length > min_length and self.area() > min_area:

			#Find point at approximate half
			split_point = split_edge[0] + split_edge.dir_vector*np.random.uniform(0.45,0.55)
			new_edges = [[],[]]
			switch = True
			
			#Find points where line starting from split point intersects other edges,
			#allocate new edges to two different lists using switch variable
			for other in self.edges:
				if other is split_edge:
					new_edges[switch].append(Edge(split_edge[0], split_point, split_edge.bordering_road))
					switch = not switch
					new_edges[switch].append(Edge(split_point, split_edge[1], split_edge.bordering_road))
				else:
					intersects = False
					try:
						x = np.linalg.solve(np.array([split_edge.n, -other.dir_vector]).T, other[0] - split_point)
						if eps < x[0] and 0 + eps < x[1] < 1 - eps:
							intersects = True
							new_point = split_point + x[0]*split_edge.n
					except np.linalg.LinAlgError:
						pass
					if intersects:
						new_edges[switch].append(Edge(other[0], new_point, bordering_road=other.bordering_road))
						new_edges[switch].append(Edge(new_point, split_point, bordering_road=False))
						switch = not switch
						new_edges[switch].append(Edge(split_point, new_point, bordering_road=False))
						new_edges[switch].append(Edge(new_point, other[1], bordering_road=other.bordering_road))	
					else:
						new_edges[switch].append(other)
			
			#Check whether both resulting polygons would border a street,
			#if not, try again with new split edge		
			for edge_set in new_edges:
				if all(not edge.bordering_road for edge in edge_set):
					if i < len_edges:
						split_edge = sorted_edges[i]
						i += 1
					else:
						return False
			else:
				return Polygon(new_edges[0], is_lot=True), Polygon(new_edges[1], is_lot=True)
		return False
			


if __name__=="__main__":
	import poly_plot as pp
	p = [np.array(x) for x in [[0,0],[0,1],[1,0.8],[1,0]]]
	poly = Polygon(p)
	p1,p2 = poly.split()
	p1.selfplot(); p2.selfplot()
	plt.show()
	
						
		
		
		
		
		
		
	
