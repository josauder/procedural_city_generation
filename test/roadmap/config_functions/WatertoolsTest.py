def main():
	import matplotlib.pyplot as plt
	
	import matplotlib.image as mpimg
	import sys, os
	sys.path.append("../../..")
	import procedural_city_generation
	
	from procedural_city_generation.roadmap.config_functions.Watertools import Watertools
	import Image
	import numpy as np
	img=np.dot(mpimg.imread(os.getcwd() + "/resources/manybodies.png")[...,:3], [0.299, 0.587, 0.144])
	
	w=Watertools(img)
	plt.imshow(img,cmap="gray")
	plt.show()
	f=w.flood(0.95,np.array([80,2]))
	plt.imshow(f, cmap="gray")
	plt.show()
	
	
	
if __name__ == '__main__':
	main()
