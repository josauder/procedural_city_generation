def input_image_setup(img_name, img2_name):
	'''	Nimmt ein Bild als input, erstellt eine "Regel-Karte". Bei der Bild-
	erstellung bedenken: Rot = Gitter, Gruen = Verzweigt, Blau = Radial, wobei ein schwarzer
	Pixel ein Zentrum definiert. '''
	#TODO: Document
	import matplotlib.image as mpimg
	import matplotlib.pyplot as plt
	import procedural_city_generation
	import os
	#TODO:translate	
	
	img = mpimg.imread(img_name)
	img2 = mpimg.imread(img2_name)
	
	import matplotlib.pyplot as plt
	path=os.path.dirname(procedural_city_generation.__file__)
	plt.imsave(path+"/temp/diffused.png",img2,cmap='gray')
	with open(path+"/temp/isdiffused.txt",'w') as f:
		f.write("False")
	
	
	img*=255
	img2*=255
	return img, img2
