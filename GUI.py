import procedural_city_generation
import sys,os
import Tkinter
from UI import *
import json

class confGUI:
	def __init__(self,modulename):
		self.modulename=modulename
	
	def call(self):
		parammodule=__import__("procedural_city_generation."+self.modulename+"."+self.modulename+"_params",globals(),locals(),["params"])
		params=parammodule.params
		
		path="./procedural_city_generation/inputs/"+self.modulename+".conf"
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

class Callapi:
	def __init__(self, modulename):
		self.modulename=modulename
	def call(self):
		main(["",self.modulename,"run"])
	
class StdoutRedirector:
	"""
	Redirects all "print" outputs from Terminal into the Tkinter window
	that is given as constructor.
	"""
	def __init__(self,label_obj):
		"""
		Parameters
		----------
		label_obj : Tkinter-Object with config method
			Any Tkinter Object whose text can be changed over label_obj.config(text=String)
		"""
		self.label_obj=label_obj
		
	def write(self,out):
		"""
		Method to be called by sys.stdout when text is written by print.
		
		Parameters
		----------
		out : String
			Text to be printed
		"""
		if not out.endswith("\n"):
			out += "\n"
		self.label_obj.config(state="normal")
		self.label_obj.insert(Tkinter.END,out)
		self.label_obj.update()
		self.label_obj.see("end")
		self.label_obj.config(state="disabled")
		
	def clear(self):
		self.label_obj.config(text='')
		self.label_obj.update()

class GUI:
	
	def __init__(self):
		self.window=Tkinter.Tk(className=" Procedural City Generation")
		self.window.minsize(width=650, height = 500)
		self.window.maxsize(width=650, height= 500)
		self.buttons=[]
		
		self.add_executable_button("Create a Roadmap","roadmap")
		self.add_executable_button("Subdivide a Roadmap into Polygons","polygons")
		self.add_executable_button("Generate 3D Data","building_generation")
		self.add_executable_button("Visualize in Blender","visualization")
		
		self.out_text=Tkinter.Text(self.window, borderwidth = 5, relief="flat", bg="black", fg="white",state="disabled")
		self.out_text.grid(row=5,sticky='EW')
		self.out_text_scrollbar=Tkinter.Scrollbar(self.window, command=self.out_text.yview)
		self.out_text_scrollbar.grid(row=5, column=1, sticky="NSW")
		self.out_text.config(yscrollcommand=self.out_text_scrollbar.set)
		sys.stdout=StdoutRedirector(self.out_text)
		self.buttons=[]
		
		self.window.mainloop()
	
	def add_executable_button(self,buttontext,modulename):
		button=Tkinter.Button(self.window, text = buttontext, command = Callapi(modulename).call)
		button.grid(row=len(self.buttons), column=0, sticky='EW')
		option_button=Tkinter.Button(self.window, text = 'Options', command = confGUI(modulename).call)
		option_button.grid(row=len(self.buttons), column=1, sticky='EW')
		self.buttons.append(button)


if __name__ == '__main__':
	pass
	GUI()
