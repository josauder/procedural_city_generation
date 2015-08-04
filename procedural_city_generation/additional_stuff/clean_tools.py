#path=procedural_city_generation.__file__
path="/home/jonathan/procedural_city_generation"
def listfiles(checkpath):
	import os
	filelist=[]
	
	liste=os.listdir(checkpath)
	counter=0
	for x in liste:
		if not os.path.isdir(checkpath+"/"+x):
			filelist.append(checkpath+"/"+x)
		else:
			filelist.extend(listfiles(checkpath+"/"+x))
	return filelist
	
	

def clean_pyc_files(checkpath):
	import os
	pyc_files= [x for x in listfiles(checkpath) if x.endswith(".pyc")]
	for pyc in pyc_files:
		os.system("rm "+pyc)
	return 0

def find_readable_files(checkpath):
	import os
	allfiles=listfiles(checkpath)
	readables=[]
	for somefile in allfiles:
		if not somefile.endswith(".pyc") and not os.path.isdir(somefile):
			readables.append(somefile)
	return readables
	
def find_TODOS(checkpath):
	allfiles=find_readable_files(checkpath)
	
	for somefile in allfiles:
		
		with open(somefile,'r') as f:
			s=f.readlines()
		
		todos=[]
		for line in s:
			if "TODO" in line:
				todos.append(line.strip())
		if len(todos)>0:
			print "\n"+somefile
			for x in todos:
				print x
	return 0


def find_in_text(checkpath,tofind):
	allfiles=find_readable_files(checkpath)
	
	for somefile in allfiles:
		
		with open(somefile,'r') as f:
			s=f.readlines()
		
		todos=[]
		for line in s:
			if tofind in line:
				todos.append(line.strip())
		if len(todos)>0:
			print "\n"+somefile
			for x in todos:
				print x
	return 0
