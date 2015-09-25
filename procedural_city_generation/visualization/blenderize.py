
try:	
	import bpy, os, sys
except:
	pass


def createtexture(name,scale,texturetype='REPEAT'):
	"""
	Creates a Blender Texture Object. Only Tested with Cycles Engine.
	
	Parameters
	----------
	name : String
		Name of this Texture
	scale : int
		How many times this Texture is to be scaled down. This Parameter still needs work.
		In the future, when 0 is passed, it is supposed to scale a Texture exactly on each polygon,
		meant to be useful e.g. when creating windows.
	texturetype : String (optional)
		currently unused
	"""
	#TODO: sticky textures 's'
	if scale==0:
		scale=40
	
	
	mat=bpy.data.materials.new(name)
	mat.use_nodes=True
	imagenode = mat.node_tree.nodes.new("ShaderNodeTexImage")
	mat.node_tree.nodes.active = imagenode
	imagenode.image=bpy.data.images.load(os.getcwd()+"/procedural_city_generation/visualization/Textures/"+name)
	imagenode.projection='BOX'
#	imagenode.vector_type='Vector'
	diffusenode=mat.node_tree.nodes["Diffuse BSDF"]
	mat.node_tree.links.new(imagenode.outputs['Color'],diffusenode.inputs[0])
	
	mappingnode=mat.node_tree.nodes.new("ShaderNodeMapping")
	mappingnode.vector_type='VECTOR'
	mappingnode.scale=(scale,scale,scale)
	mat.node_tree.links.new(mappingnode.outputs[0],imagenode.inputs[0])

	
	coordsnode= mat.node_tree.nodes.new("ShaderNodeTexCoord")
	mat.node_tree.links.new(coordsnode.outputs['Generated'],mappingnode.inputs[0])
	#materialslist.append(mat)
	return mat

def createmesh(verts,faces,texture):
	"""
	Creates a Blender mesh from a list of vertices and faces while assigning a texture object
	
	Parameters
	----------
	verts : iterable<iterable<float(shape(3,))>> 
		Iterable of 3D-Coordinates of vertices
	faces : iterable<iterable<int>>
		Iterable of Iterables of the indices of the verts which make up each face
	texture : Blender texture object
	"""
	me=bpy.data.meshes.new('mesh')
	ob=bpy.data.objects.new('mesh',me)
	me.from_pydata(verts,[], faces)
	me.update(calc_edges=True)
	me.materials.append(texture)
	return ob
	



def createobject(verts,faces,texname,texscale,shrinkwrap):
	"""
	Creates a Blender object for each mesh. Each mesh is (after the
	building_generation submodule) a list of all vertices and faces which share
	the same texture (in order to make blender start up in reasonable time).
	Shrinkwrapped textures will be blender-shrinkwrapped (projected on to)
	the surface mesh. 
	
	Parameters
	----------
	verts : iterable<iterable<float(shape(3,))>> 
		Iterable of 3D-Coordinates of vertices
	faces : iterable<iterable<int>>
		Iterable of Iterables of the indices of the verts which make up each face
	texturename : String
		Must be identical with the name of the image in /visualization/Textures
	shrinkwrap: boolean
		If true, then this mesh will be triangulated and then shrinkwrapped. 
		It makes sense to have this	attribute set as true for Roads and Floortypes.
	
	"""
	tex=createtexture(texname,texscale)
	ob=createmesh(verts,faces,tex)
	
	if shrinkwrap:
		ob.modifiers.new("Triangulate", type="TRIANGULATE")
		triangulate=ob.modifiers["Triangulate"]
	
		ob.modifiers.new("Subsurf", type="SUBSURF")
		subsurf=ob.modifiers["Subsurf"]
		subsurf.subdivision_type="SIMPLE"
		subsurf.levels=6
		subsurf.render_levels=4
	
		ob.modifiers.new("Shrinkwrap", type='SHRINKWRAP')
		wrap=ob.modifiers['Shrinkwrap']
		wrap.wrap_method='PROJECT'
		wrap.use_negative_direction=True
		wrap.use_project_z=True
		wrap.target=bpy.context.scene.objects['Floormesh']
		wrap.offset=0.03

	bpy.context.scene.objects.link(ob)

def setupscenery():
	"""
	Sets up the lighting and render engine.
	In the future could provide options like "time of day","weather",
	"renderengine".
	"""
	bpy.context.scene.render.engine="CYCLES"
	try:
		startup_cube=bpy.context.scene.objects.get("Cube")
		bpy.context.scene.objects.unlink(startup_cube)
	except:
		pass
		
	bpy.data.lamps["Lamp"].type="SUN"


def main(points,triangles,polygons):
	"""
	Intended to run in Blender. This means that this script must be written
	in Python 3 conformity. Works by reading and unpickling /outputs/buildings.txt
	and /outputs/<correct-heightmap-name>.txt and creating Blender Polygons for each of these.
	
	Run from console (from parent direcotry) with
	``blender --python /procedural_city_generation/visualization/blenderize.py``
	
	"""
	
	setupscenery()
	
	me=bpy.data.meshes.new('Floormesh')
	ob=bpy.data.objects.new('Floormesh',me)
	me.from_pydata(points,[], triangles)
	me.update(calc_edges=True)
	
	#TODO: Not flexible code.
	me.materials.append(createtexture("Floor02.jpg",100,True))

	bpy.context.scene.objects.link(ob)
	
	
	
	
	floor_has_texture=False
	for poly in polygons:
		verts,faces, texname, texscale, shrinkwrap= poly
		createobject(verts,faces,texname,texscale,shrinkwrap)
		
		
	
if __name__ == '__main__':
	
	import pickle
	
	path=os.getcwd()+"/procedural_city_generation"
	
	try:
		with open(path+"/temp/heightmap_in_use.txt",'r') as f:
			filename=f.read()
		with open(path+"/temp/"+filename,'r') as f:
			points, triangles = pickle.loads(f.read().encode('utf-8'))
		with open(path+"/outputs/buildings.txt",'r') as f:
			polygons=pickle.loads(f.read().encode('utf-8'))
		main(points,triangles,polygons)
	except IOError:
		print( "Input could not be located. Try to run the previous program in the chain first.")

	
