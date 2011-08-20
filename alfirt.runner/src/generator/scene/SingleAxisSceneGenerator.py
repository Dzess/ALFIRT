'''
Created on Aug 11, 2011

@author: Piotr
'''
from generator.data.SceneDescription import SceneDescription
from generator.data.ObjectPose import ObjectPose
from mathutils import Vector
import math

class SceneGeneratorBase(object):
    '''
        Base abstract class for generating scenes
    '''
    def prepareScenes(self):
        raise NotImplementedError("This is abstract method")


class SingleAxisSceneGenerator(SceneGeneratorBase):
    '''
    Generates @see: SceneDescription object from the @see: GeneratorDescription object.
    Uses only the alfa OR beta angels for generation, thus camera moves in the 
    ONE surface !
    '''


    def __init__(self, generatorDesc, initCamera, initAnchor=None):
        '''
        @param generatorDesc: instance of the @see: GeneratorDescription class.
        @param initCamera: initial position of the camera @see: ObjectPose
        @param initAnchor: initial position of the anchor (object). If not provided
        then it is assumed that anchor is in the beginning of the coordinate system
            @see: ObjectPose
        '''
        if initAnchor == None:
            initAnchor = ObjectPose([0, 0, 0], [0, 0, 0])

        self.generatorDesc = generatorDesc
        self.initCamera = initCamera
        self.initAnchor = initAnchor


    def __getCount(self, interval):
        return ((interval.stop - interval.start) / interval.step) if interval.step != 0 else 0

    def prepareScenes(self):
        '''
            Gets the list of @see: SceneDescription with the provieded scene
        '''
        # TODO
        alfaCount = self.__getCount(self.generatorDesc.alfa)

        result = []
        upTo = int(math.floor(alfaCount)) + 1
        for i in range(0, upTo):
            result.append(SceneDescription(None, None))
        return result


