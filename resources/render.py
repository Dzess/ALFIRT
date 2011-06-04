"""
	In blender script for importing the X3D scene description and simple rendering it.
	@author Piotr Jessa
"""
import bpy
from bpy import context
from bpy import ops
from io_scene_x3d import import_x3d

print ("ALFIRT: start of rendering")

#Parameters of the image
# TODO: this image parameters must from code generated
formatInput = ".x3d"
formatOutput = ".bmp"
name = "violin" 
input ="models/"
output ="renders/"

# Get the names right
fileNameInput = input + name  + formatInput
fileNameOutput = output + name + formatOutput

# Create the new scene wihout lighting or cube or anyting
# the way with the new scene would be better i guess, but render does not work
oldScn  = bpy.data.scenes['Scene']
for obj in bpy.context.visible_objects:
	oldScn.objects.unlink(obj)



#Import - b2.57
import_x3d.load_web3d(fileNameInput) 

# Add sample diffuse light - caled here area light 
# TODO: set the light source behind the camera (view point)
areaLampVector = [0,0,20] 
bpy.ops.object.lamp_add(type='HEMI',location=areaLampVector)

# get render settings
renderSettings = context.scene.render
# TODO: make sure the render uses the nice things

# Get the render
ops.render.render(scene='Scene')
img = bpy.data.images['Render Result']

# TODO: get the properties of the saved file
img.save_render(filepath=fileNameOutput)

print ("ALFIRT: end of rendering")