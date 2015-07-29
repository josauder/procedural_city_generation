import procedural_city_generation
import sys,os
import Tkinter
path=os.path.dirname(procedural_city_generation.__file__)
sys.path.append(path)



def roadmap():
	from procedural_city_generation.roadmap import main as roadmap_main
	roadmap_main.main()

def polygons():
	from procedural_city_generation.polygons import main as polygon_main
	polygon_main.main(None,True)

def building_generation():
	from procedural_city_generation.building_generation import main as building_generation_main
	
	import pickle
	with open(path+"/outputs/polygons.txt",'r') as f:
		polygons=pickle.loads(f.read())
	
	building_generation_main.main(polygons)
	

def visualization():
	
	
	os.system("blender --python "+path+"/visualization/blenderize.py")

def confGUI(path , params):
	import json
	
	with open(path,'r') as f:
		s=json.loads(f.read())
		
	confwindow=Tkinter.Tk(className=path + " Options")
	
	i=1
	
	entryfields=[]
	
	Tkinter.Label(confwindow,text="Name", bd=2, pady=2).grid(row=0, column=0, sticky='EW')
	Tkinter.Label(confwindow,text="Description", bd=2, pady=2).grid(row=0, column=1, sticky='EW')
	Tkinter.Label(confwindow,text="Value", bd=2, pady=2).grid(row=0, column=2, sticky='EW')
	
	for param in params:
		name=Tkinter.Label(confwindow,text=param.name,bd=1,relief="raised",height=1).grid(row=i,column=0,sticky='EW')
		description=Tkinter.Label(confwindow,text=param.description,bd=1,relief="raised").grid(row=i,column=1, sticky='EW')
		entry=Tkinter.Entry(confwindow, bd=3)
		entryfields.append(entry)
		entry.insert(0,s[param.name])
		entry.grid(row=i,column=2,pady=2)
		
		i+=1
	
	def restore_default():
		for i in range(len(params)):
			entryfields[i].delete(0,1000)
			entryfields[i].insert(0,params[i].default)
	
	def done():
		new_s=dict([])
		for i in range(len(params)):
			try:
				new_s[params[i].name]=eval(entryfields[i].get())
			except:
				new_s[params[i].name]=entryfields[i].get()
		with open(path,'w') as f:
			f.write(json.dumps(new_s))
		confwindow.destroy()
		return 0
		
	restore_default_button=Tkinter.Button(confwindow,text= "Restore Default", command=restore_default ,bd=3)
	done_button=Tkinter.Button(confwindow, text= "Done", command=done ,bd=3)
	
	restore_default_button.grid(row=i, column=0)
	done_button.grid(row=i,column=2)
	
	confwindow.mainloop()




def roadmapconf():
	from procedural_city_generation.roadmap.roadmap_params import params as roadmapparams
	confGUI(path+"/inputs/roadmap.conf", roadmapparams)

def polygonconf():
	from procedural_city_generation.polygons.polygons_params import params as polygonsparams
	confGUI(path+"/inputs/polygons.conf", polygonsparams)

def building_generationconf():
	from procedural_city_generation.building_generation.building_generationparams_params import params as building_generationparams
	#TODO
	confGUI(path+"/inputs/polygons.conf", building_generationparams)
	
	
	

def visualizationconf():
	from procedural_city_generation.visualization_params import params as visualizationparams
	#TODO
	confGUI(path+"inputs/polygons.conf", visualizationparams)


def GUI():
	
	import Tkinter
	from tkFileDialog import askopenfilename
	
	window=Tkinter.Tk(className=" Procedural City Generation")
	
	roadmap_button=Tkinter.Button(window, text = 'Create a Roadmap', command = roadmap)
	roadmap_button.grid(row=1, column=0, sticky='EW')
	roadmap_option_button=Tkinter.Button(window, text = 'Options', command = roadmapconf)
	roadmap_option_button.grid(row=1, column=1, sticky='EW')
	
	polygon_button=Tkinter.Button(window, text = 'Subdivide a Roadmap in Polygons', command = polygons)
	polygon_button.grid(row=2, column=0 ,sticky='EW')
	roadmap_button=Tkinter.Button(window, text = 'Options', command = polygonconf)
	roadmap_button.grid(row=2, column=1, sticky='EW')
	
	polygon_button=Tkinter.Button(window, text = 'Generate 3D Data', command = building_generation)
	polygon_button.grid(row=3, column=0 ,sticky='EW')
	roadmap_button=Tkinter.Button(window, text = 'Options', command = building_generationconf)
	roadmap_button.grid(row=3, column=1, sticky='EW')
	
	polygon_button=Tkinter.Button(window, text = 'Visualize in Blender', command = visualization)
	polygon_button.grid(row=4, column=0 ,sticky='EW')
	roadmap_button=Tkinter.Button(window, text = 'Options', command = visualizationconf)
	roadmap_button.grid(row=4, column=1, sticky='EW')

	
	
#	filename=askopenfilename()
#	print filename
	
	
	window.mainloop()


if __name__ == '__main__':
	pass
	GUI()
