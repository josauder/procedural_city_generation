import numpy as np
from Polygon import Polygon, Edge

def getFoundation(poly, grid_width=0.05, min_area=0.25, eps=10**-5):
	
	max_rect = False
	
	for base in sorted([edge for edge in poly.edges if edge.bordering_road],
							key=lambda x: -x.length):
		height = grid_width
		done = False
		while not done:
			print "working"
			cuts = []
			for other in poly.edges:
				if other is not base:
					x = [0,0]
					try:
						x = np.linalg.solve(np.array(((base.dir_vector), (other.dir_vector))).T, 
														other[0] - (base[0] + height * base.n))
					except np.linalg.LinAlgError:
						pass
					print "Solution: ", x
					if eps < x[1] < 1 - eps:
						#intersection found
						if x[0] < eps:
							cuts.append(0)
						elif x[0] > 1 - eps:
							cuts.append(1)
						else:
							cuts.append(x[0])
				print "Cuts: ", cuts
				if len(cuts) == 2:
					width = abs(base.length*cuts[1] - base.length*cuts[0])
					this_area = width * height
					print "Area: %s" %(this_area)
					if this_area > max_area:
						max_area = this_area
						rect_edges = new_cuts
						rect_height = height
						rect_base = base
					height += grid_width
					
				else:
					done = True
					break
	if rect_height:
		p1 = rect_base[0] + x[1] * rect_base.dir_vector
		p2 = rect_base[0] + x[0] * rect_base.dir_vector
		p3 = p2 + height * rect_base.n
		p4 = p1 + height * rect_base.n
		
		return Polygon([p1,p2,p3,p4])
	else:
		return False
	
if __name__=="__main__":
	pass			
						
							
				
		
					
		
			
	
					
	
		
		
		
	
	
