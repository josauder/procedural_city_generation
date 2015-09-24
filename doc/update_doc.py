
def main():
	
	
	
	l=len("procedural_city_generation")+1
	import os, sys
	
	os.system("sphinx-apidoc -o . ..")
	
	for x in os.listdir(os.getcwd()):
		if x.endswith(".rst"):
			print x
			x2=x
			if "procedural_city_generation.procedural_city_generation" in x:
				x2=x[l:]
				os.system("mv "+x+" "+x2)
			
			with open(x2,'r') as f:
				filecontent=f.read()
			
			filecontent=filecontent.replace("procedural_city_generation.procedural_city_generation","procedural_city_generation")
			with open(x2,'w') as f:
				f.write(filecontent)
	
	script=[
	"make html",
	"mkdir temp",
	"cp ../.git temp",
	"cp ../.gitignore temp",
	"cd temp",
	"git checkout gh-pages",
	"rm -R *",
	"cp -R ../_build/html/* .",
	"git add --all",
	"git commit -m \" updated gh-pages with update_doc.py\"",
	"git push",
	"cd ..",
	"rm -R temp",
	]
	
	for command in script:
		os.system(commant)
	
	return 0

if __name__ == '__main__':
	main()

