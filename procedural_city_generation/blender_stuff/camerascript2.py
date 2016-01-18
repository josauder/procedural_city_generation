import bpy
import math

start=22


bpy.data.scenes["Scene"].render.resolution_x=360
bpy.data.scenes["Scene"].render.resolution_y=240

bpy.ops.object.empty_add(type='CUBE')
camera=bpy.context.scene.objects['Camera']
camera.location.x=0
camera.location.y=0
camera.location.z=start
camera.rotation_euler.x=0
camera.rotation_euler.y=0
camera.rotation_euler.z=0

def render(i):
    bpy.context.scene.frame_set(i)
    bpy.context.scene.render.filepath = "/home/jonathan/Desktop/Mathesis/Testfolder/" + str(i).zfill(4)
    bpy.ops.render.render(write_still=True)


empty=bpy.context.scene.objects['Empty']

empty.select=True
camera.select=True
bpy.context.scene.objects.active = empty
bpy.ops.object.parent_set()


for i in range(45):
    empty.rotation_euler.x+=1/360*2*math.pi
    render(i)

bpy.ops.object.parent_clear(type='CLEAR')
empty.rotation_euler.x=0
camera=bpy.context.scene.objects['Camera']
camera.location.y=-.707*start
camera.location.z=.707*start
camera.rotation_euler.x+=45/180*math.pi
empty.location.z=.707*start


empty=bpy.context.scene.objects['Empty']
empty.select=True
camera.select=True
bpy.context.scene.objects.active = empty
bpy.ops.object.parent_set()


for i in range(360):
    empty.location.x+=1/360*start/2
    empty.location.y+=1/360*start/2
    empty.location.z+=-1/360*start/10

    empty.rotation_euler.z+=1/180*math.pi
    render(i+45)

