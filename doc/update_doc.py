
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
	
	os.system("make html")
	os.chdir("./_build/html")
	print "Updating of documentation done, you should be able to view the documentation in your browser at the address 'localhost:8080'"
	os.system("python -m SimpleHTTPServer 8080")
	
	return 0

if __name__ == '__main__':
	main()

