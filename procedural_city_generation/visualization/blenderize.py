
	
import bpy, os
def createtexture(name,scale,texturetype='REPEAT'):
	#TODO: sticky textures 's'
	if isinstance(scale,str):
		scale=1000
	
	
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
	me=bpy.data.meshes.new('mesh')
	ob=bpy.data.objects.new('mesh',me)
	me.from_pydata(verts,[], faces)
	me.update(calc_edges=True)
	me.materials.append(texture)

	return ob
	



def createbuilding(verts,faces,texname,texscale,shrinkwrap):
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
#	else:
#		subsurf.levels=6
#		subsurf.render_levels=6
	
	
		ob.modifiers.new("Shrinkwrap", type='SHRINKWRAP')
		wrap=ob.modifiers['Shrinkwrap']
		wrap.wrap_method='PROJECT'
		wrap.use_negative_direction=True
		wrap.use_project_z=True
		wrap.target=bpy.context.scene.objects['mesh']
		wrap.offset=0.03

	bpy.context.scene.objects.link(ob)
#	allmeshes.append(ob)
	
	
	
	
def main():
	
	import pickle
	
	path=os.getcwd()+"/procedural_city_generation"
	
#	import sys
#	sys.path.append(os.getcwd())
#	import procedural_city_generation.visualization
	with open(path+"/temp/heightmap_in_use.txt",'r') as f:
		filename=f.read()
	with open(path+"/temp/"+filename,'r') as f:
		points, triangles = pickle.loads(f.read().encode('utf-8'))
	
	bpy.context.scene.render.engine="CYCLES"
	try:
		startup_cube=bpy.context.scene.objects.get("Cube")
		bpy.context.scene.objects.unlink(startup_cube)
	except:
		pass
		
	bpy.data.lamps["Lamp"].type="SUN"
	
	me=bpy.data.meshes.new('mesh')
	ob=bpy.data.objects.new('mesh',me)
	me.from_pydata(points,[], triangles)
	me.update(calc_edges=True)
	bpy.context.scene.objects.link(ob)
	
	with open(path+"/outputs/buildings.txt",'r') as f:
		polygons=pickle.loads(f.read().encode('utf-8'))
	
	for poly in polygons:
		faces, verts, texname, texscale, shrinkwrap= poly
		createbuilding(faces,verts,texname,texscale,shrinkwrap)
		
		
		
if __name__ == '__main__':
	main()


