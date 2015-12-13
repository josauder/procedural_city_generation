def input_image_setup(rule_image_name, density_image_name):
	'''	
	Loads the rule-image and population-density-image from the filesystem.
	Saves the density image in /temp/ folder so that it could be ensured.
	 
	Parameters
	----------
	rule_image_name: String
		Name of the rule_image specified in Parameters
	density_image_name: String
		Name of the density_image specified in Parameters

	Returns
	--------
	rule_img: np.ndarray
		Rule-image as numpy array
	density_img: np.ndarray
		Density-image as numpy array
	'''

	#TODO: Document
	import matplotlib.image as mpimg
	import procedural_city_generation
	import os
	path=os.path.dirname(procedural_city_generation.__file__)

	rule_img = mpimg.imread(path+"/inputs/rule_pictures/"+rule_image_name)
	density_img = mpimg.imread(path+"/inputs/density_pictures/"+density_image_name)

	import matplotlib.pyplot as plt
	plt.imsave(path+"/temp/"+density_image_name.split(".")[0]+"diffused.png",density_img,cmap='gray')
	with open(path+"/temp/"+density_image_name.split(".")[0]+"isdiffused.txt",'w') as f:
		f.write("False")
	
	
	rule_img*=255
	density_img*=255
	return rule_img, density_img
