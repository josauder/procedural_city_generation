import bpy
import math
frames=180

#Add Empty
bpy.ops.object.empty_add(type='CUBE')
camera=bpy.context.scene.objects['Camera']
camera.location.x=0
camera.location.y=0
camera.location.z=50
camera.rotation_euler.x=0
camera.rotation_euler.y=0
camera.rotation_euler.z=0

empty=bpy.context.scene.objects['Empty']

empty.select=True
camera.select=True
bpy.context.scene.objects.active = empty
bpy.ops.object.parent_set()

def rad(deg):
    return deg/360*2*math.pi

def getCam(i):

    xT=yT=zT=xR=yR=zR=0
    d=1
    if i<60:
        xR=rad(1)
        d-=0.01
#        zT=-0.05
    zR+=rad(1)
    if i == 10:
        camera.removeParent()

    if i>360:
        d+=0.01

    return xT, yT, zT, xR, yR, zR, d



for i in range(frames):
    xT, yT, zT, xR, yR, zR, d= getCam(i)

    empty.location.x+=xT
    empty.location.y+=yT
    empty.location.z+=zT
    empty.scale.z=+d
    empty.rotation_euler.x+=xR
    empty.rotation_euler.y+=yR
    empty.rotation_euler.z+=zR

def render(i):
    bpy.context.scene.frame_set(i)
    bpy.context.scene.render.filepath = "/home/jonathan/Desktop/Mathesis/Testfolder/" + str(i).zfill(4)
    bpy.ops.render.render(write_still=True)

