import os

def parent_path(depth=1):
	"""
	Return path to directory which is depth
	levels above
	"""
	path = os.path.abspath(__file__)
	n = 0
	for i in xrange(1,len(path)+1):
		if path[-i] == "/":
			n += 1
		if n == depth:
			return path[:len(path)-i]

if __name__=="__main__":
	print "This path: /n" + os.path.abspath(__file__)
	for i in range(1,4):
		print "Parent path, depth = %s:/n" %(i) + parent_path(depth=i)
