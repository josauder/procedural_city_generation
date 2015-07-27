Small manual on current state of project

Dependencies:
scipy,numpy,Blender(only tested with 2.69 so far)

Current bugs:
-center of radial rule not in the actual center

Current TODOS:















There are 3 main parts of this project at the moment:

1) Creation of Strassennetz
2) Creation of Data for Blender
3) Blender startup script

___________1__________
To create a Strassennetz open /stadt/Strassennetz/PythonVersion/conf.txt to see a list of all input parameters.
Run /stadt/Strassennetz/PythonVersion/main.py to start the creation.


Important Parameters:
	-rahmen: Destines size of city. Strassennetz can easily create ones with [100,100] but Blender can hardly handle [20,20] as of now.
	
	-regelbild_name: see directory /stadt/Strassennetz/PythonVersion/Regelbilder for examples. Any image with distinct RGB values will do. Red=gitter, Green=verzweigt, Blue=radial.

	-bevoelkerungsbild_name: see directory /stadt/Strassennetz/PythonVersion/Bevoelkerungsdichtebilder for examples. Any grayscale image will do. White=high pop.density, Black=low pop.density

	-Heightmap_name: see directory /stadt/Strassennetz/PythoNVersion/Heightmaps for examples. Any grayscale image will do. If "random" is given as input, a new random map will be created with /stadt/Polygone/randommap.py. However, the randommap generator sucks as of now. If you add a new image to the folder, the first time the program runs with it, you will be asked to enter a height difference. Recommended is "1", as we roughly stick to the scale 1=100meters.

	-plot: if 1, then you will see the growth of the Strassennetz live

	-savefig: if 1, then the image will be saved along the output.txt in /PythonVersion/Outputs. Not necessary if plot is 1 already.


_________2__________
Run /stadt/Polygone/main to start the creation. If you want to see the matplotlib graphic to the subdivided polygons, start with main.main(True)
Note that the building creation at the moment is not working as inteded (also rather slow).

_________3_________
change into /stadt/Visualisierung directory
run blender --python blenderize.py
Prepare for startup times of about 1 minute if you run with more than 700 Buildings.
Press render to render


