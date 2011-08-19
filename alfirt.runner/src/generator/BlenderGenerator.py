'''
Created on 10-05-2011

@author: Piotr
'''
import os

class BlenderGenerator(object):
    '''
    Generates the .py file for rendering complaint with blender 2.57.
    '''

    def __findAlfirtPath(self):
        '''
            Gets the path to render.py located in resources
        '''
        path = os.getcwd()
        path = os.path.normpath(path)

        folders = []
        while True:
            path, folder = os.path.split(path)

            if folder != "":
                folders.append(folder)
            else:
                if path != "":
                    folders.append(path)
                break

        folders.reverse()

        sum_coll = []
        for i in folders:
            if i == "alfirt.runner":
                sum_coll.append(i)
                break
            else :
                sum_coll.append(i)

        sum_coll.append('resources')
        sum_coll.append('render.py')

        if os.name == 'posix':
            #sum_coll.remove('/')
            alfirt_path = "/".join(sum_coll)
            alfirt_path = os.path.normpath(alfirt_path)
        else :
            raise NotImplementedError("Implement other than posix standards")

        return alfirt_path

    def __init__(self, generatorDescription):
        '''
        Constructor. Assumes the file location in the resources file
        render.py
        '''

        self.renderFileLocation = self.__findAlfirtPath()
        self.generatorDescription = generatorDescription


    def prepareRender(self, sceneDescription):
        '''
        Prepares the render script for generating.
        @param sceneDescription: description of the scene, mostly involving 
        environmental settings such as cameras, light sources.
        @return: the string with the blender python script for provided elements.
        '''

        blender_script = open(self.renderFileLocation, mode='r').readlines()

        print(blender_script)



