'''
Created on Aug 20, 2011

@author: Piotr
'''
from generator.data.GeneratorDescription import GeneratorDescription

import os

class RunnerBase(object):
    '''
        Abstract base class for runner
    '''
    def execute(self):
        raise NotImplementedError("This is abstract method")

class BlenderRunner(RunnerBase):
    '''
        Class uses the injected scene generator and @see: GeneratorDescription objects
    '''

    def __init__(self, generatorDescription, sceneGenerator, renderGenerator):
        '''
        Constructor
        @param generatorDescription: object of class @see: GeneratorDescription
        @param sceneGenerator: implementation of the @see: SceneGeneratorBase
        @param renderGenerator: implementation of the @see: RenderGeneratorBase
        '''
        self.generatorDescription = generatorDescription
        self.sceneGenerator = sceneGenerator
        self.renderGenerator = renderGenerator

        self._base_command = "blender -b --python "

    def __buildCommand(self, inputScript):
        return self._base_command + inputScript

    def __getRenderScript(self):
        # TODO: write saving script from renderGeratorBase to file and reading its path
        pass

    def execute(self):
        # get all the renderings
        # TODO: write the getting rendering from the render generator base 

        inputScript = ""

        # get the rendering
        print("alfirt.runner:" + "started rendering")
        command = self.__buildCommand(inputScript)
        stream = os.popen(command)

        # print the log of the rendering
        print(stream.read())

