def createtexture(name,texturetype='REPEAT'):
	mat=bpy.data.materials.new(name)
	mat.use_nodes=True
	imagenode = mat.node_tree.nodes.new("ShaderNodeTexImage")
	mat.node_tree.nodes.active = imagenode
	imagenode.image=bpy.data.images.load(os.getcwd()+"/Textures/"+name)
	imagenode.projection='BOX'
#	imagenode.vector_type='Vector'
	diffusenode=mat.node_tree.nodes["Diffuse BSDF"]
	mat.node_tree.links.new(imagenode.outputs['Color'],diffusenode.inputs[0])
	
	mappingnode=mat.node_tree.nodes.new("ShaderNodeMapping")
	mappingnode.vector_type='VECTOR'
	mappingnode.scale=(10,10,10)
	mat.node_tree.links.new(mappingnode.outputs[0],imagenode.inputs[0])

	
	coordsnode= mat.node_tree.nodes.new("ShaderNodeTexCoord")
	mat.node_tree.links.new(coordsnode.outputs['Generated'],mappingnode.inputs[0])
	materialslist.append(mat)

def createmesh(verts,texture,faces):
	me=bpy.data.meshes.new('mesh')
	ob=bpy.data.objects.new('mesh',me)
	me.from_pydata(verts,[], faces)
	me.update(calc_edges=True)
	try:
		me.materials.append(texture)
	except:
		pass
	return ob
	



def createbuilding(inputstring,road=False):
	
	inputstring=inputstring.split("\n")
	inputstring.pop()
	
	allmeshes=[]
	
	vertices=[]
	faces=[]
	texture=None
	for line in inputstring:
		words=line.split(" ")
		
		#If line is integer:
		if len(words)==1:
			if len(vertices)!=0:
				allmeshes.append(createmesh(vertices,texture,faces))
			texture=materialslist[int(words[0])]
			faces=[]
			vertices=[]
		else:
			verts=[float(x) for x in words if x is not '']
			coords=[]
			
			face=[]
			for i in range(len(verts)//3):
				face.append(len(vertices))
				vertices.append((verts[3*i],verts[3*i+1],verts[3*i+2]))
			faces.append(face)
	#####FLOOR#####
	floor=createmesh(vertices,texture,faces)
	bpy.context.scene.objects.active=floor
	
	
	floor.modifiers.new("Triangulate", type="TRIANGULATE")
	triangulate=floor.modifiers["Triangulate"]
	
	floor.modifiers.new("Subsurf", type="SUBSURF")
	subsurf=floor.modifiers["Subsurf"]
	subsurf.subdivision_type="SIMPLE"
	if not road:
		subsurf.levels=3
		subsurf.render_levels=4
	else:
		subsurf.levels=6
		subsurf.render_levels=6
	
	
	floor.modifiers.new("Shrinkwrap", type='SHRINKWRAP')
	wrap=floor.modifiers['Shrinkwrap']
	wrap.wrap_method='PROJECT'
	wrap.use_negative_direction=True
	wrap.use_project_z=True
	wrap.target=bpy.context.scene.objects['mesh']
	wrap.offset=0.03
	if road:
		wrap.offset=0.02
	bpy.context.scene.objects.link(floor)
#	allmeshes.append(floor)
	
	if len(allmeshes)>0:
		for me in allmeshes:
			bpy.context.scene.objects.link(me)
			me.select=True
	
		bpy.context.scene.objects.active = allmeshes[0]
		bpy.ops.object.join()
	
		allmeshes[0].select=False
	
def fromstring(inputstring):
	inputstring=inputstring.split("_\n")
	
	[createtexture(x) for x in inputstring[0].split("\n") if x is not '']
	inputstring.pop(0)
	
	l=len(inputstring)
	for i in range(l):
		if i<(l-1):
			createbuilding(inputstring[i])
		else:
			createbuilding(inputstring[i],True)
def main():
	import os
	import pickle
	
	path=os.getcwd()+"/procedural_city_generation"
	
	with open(path+"/temp/heightmap_in_use.txt",'r') as f:
		filename=f.read()
	with open(path+"/temp/"+filename,'r') as f:
		points, triangles = pickle.loads(f.read().encode('utf-8'))
	
	
	import bpy
	bpy.context.scene.render.engine="CYCLES"
	startup_cube=bpy.context.scene.objects.get("CUBE")
	bpy.context.scene.objects.unlink(startup_cube)
	
	bpy.data.lamps["Lamp"].type="SUN"
	
	me=bpy.data.meshes.new('mesh')
	ob=bpy.data.objects.new('mesh',me)
	me.from_pydata(points,[], triangles)
	me.update(calc_edges=True)
	bpy.context.scene.objects.link(ob)
	
	
	'''
	with open(os.getcwd()+"/../Polygone/rahmen.txt",'r') as f:
		rahmen=f.read()
	rahmen=[float(x) for x in rahmen.split(" ") if x is not '']
	
	bpy.context.scene.camera.location.x=rahmen[0]
	bpy.context.scene.camera.location.y=-rahmen[1]
	bpy.context.scene.camera.location.z=rahmen[1]*rahmen[0]/25
	
	
	
		
	name=os.getcwd()+"/poly.txt"
	with open(name,"r") as f:
		inputstring=f.read()
	
	a=time.time()
	fromstring(inputstring)
	me.materials.append([x for x in materialslist if  ("oor" in x.name) and ("02" in x.name)][0])

	print (time.time()-a)
	
	
	return 0
	'''
if __name__ == '__main__':
	main()


