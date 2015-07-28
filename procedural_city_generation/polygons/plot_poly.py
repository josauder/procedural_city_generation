import matplotlib.pyplot as plt

def plot_edge(edge, c):
	plt.plot((edge[0][0], edge[1][0]),(edge[0][1], edge[1][1]), c)
	
	
def plot_poly(poly, mode="type"):
	if mode == "type":
		t = poly.poly_type
		
		if t == "lot" or t=="block":
			for edge in poly.edges:
				plot_edge(edge, "g")
		elif t == "road":
			for edge in poly.edges:
				plot_edge(edge, "k")
		else:
			for edge in poly.edges:
				plot_edge(edge, "r")
	elif mode == "borders":
		for edge in poly.edges:
			if edge.bordering_road:
				plot_edge(edge, 'k')
			else:
				plot_edge(edge, 'r')
	else:
		for edge in poly.edges:
			plot_edge(edge, mode)
			
