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
        self._tokens = {}
        self._renderFileLocation = self.__findAlfirtPath()

        if generatorDescription is None :
            raise ValueError("GeneratorDescription must be provided")

        self.generatorDescription = generatorDescription

        # set up tokens basing on the generator descriptor
        self.__putToken('INPUT_FORMAT', self.generatorDescription.inputFormat)
        self.__putToken('OUTPUT_FORMAT', self.generatorDescription.outputFormat)

    def __replaceTokens(self, line):
        '''
            Searches line for token, and replaces it
        Tokens are defined in self.tokens
        '''
        for key, value in self._tokens.items():
            line = line.replace(key, value)

        return line

    def __putToken(self, key, value):
        self._tokens[key] = value

    def prepareRender(self, sceneDescription):
        '''
            Prepares the render script for generating.
        @param sceneDescription: description of the scene, mostly involving 
                                 environmental settings such as cameras, light sources.
        @return: the string with the blender python script for provided elements.
        '''

        blender_script = open(self._renderFileLocation, mode='r').readlines()

        # include scene description element injecting
        # TODO: implement getting things from scene description

        output_lines = []
        for line in blender_script:
            new_line = self.__replaceTokens(line)
            output_lines.append(new_line)

        output = "".join(output_lines)
        return output
