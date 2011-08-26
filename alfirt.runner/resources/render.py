'''
	In blender script for importing the X3D scene description and simple rendering it.
	Requires Python 3.x
	Tested with Blender 2.57b
	@author Piotr Jessa
	@contact: dzesse@gmail.com
	@version: 0.1
'''

import bpy
import os
from bpy import context
from bpy import ops
from io_scene_x3d import import_x3d

def main():
    '''
        Main code that render the file
    '''

    #Parameters of the image
    formatInput = "INPUT_FORMAT"
    formatOutput = "OUTPUT_FORMAT"
    name = "FILE_NAME"
    inputFolder = "INPUT_FOLDER"
    outputFolder = "OUTPUT_FOLDER"
    fileNameInput = os.path.join(inputFolder, name + formatInput)
    fileNameOutput = os.path.join(outputFolder, name + formatOutput)

    # Create the new scene without lighting or cube or anything
    # the way with the new scene would be better i guess, but render does not work
    oldScn = bpy.data.scenes['Scene']
    for obj in bpy.context.visible_objects:
        oldScn.objects.unlink(obj)

    #Import - b2.57
    import_x3d.load_web3d(fileNameInput)

    # Add sample diffuse light - called here area light 
    # TODO: set the light source behind the camera (view point)
    areaLampVector = [0, 0, 20]
    bpy.ops.object.lamp_add(type='HEMI', location=areaLampVector)

    # get render settings
    renderSettings = context.scene.render
    # TODO: make sure the render uses the nice things

    # Get the render
    ops.render.render(scene='Scene')
    img = bpy.data.images['Render Result']

    # TODO: get the properties of the saved file
    img.save_render(filepath=fileNameOutput)


# go with the render script
print ("ALFIRT: start of rendering")
main()
print ("ALFIRT: end of rendering")
