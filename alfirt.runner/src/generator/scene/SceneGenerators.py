'''
Created on Aug 11, 2011

@author: Piotr
'''
from generator.data.SceneDescription import SceneDescription
from generator.data.ObjectPose import ObjectPose
from mathutils import Vector
from math import cos, sin, sqrt, radians, floor

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
    roundPrecision = 15

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

        # getting the radius thing
        cameraX = float(self.initCamera.translate[0])
        cameraY = float(self.initCamera.translate[1])
        radiusXY = sqrt(cameraX * cameraX + cameraY * cameraY)
        self.radius = radiusXY
        print("Radius: " + str(self.radius))

    def __getCount(self, interval):
        return ((interval.stop - interval.start) / interval.step) if interval.step != 0 else 0


    def __getScene(self, i, alfaValue):

        # translation for circular movement
        x = round(cos(radians(alfaValue)), SingleAxisSceneGenerator.roundPrecision) * self.radius
        y = round(sin(radians(alfaValue)), SingleAxisSceneGenerator.roundPrecision) * self.radius

        # rotation for circular movement
        r = radians(90 + alfaValue)

        # create the translation for the camera
        translate = [x, y, self.initCamera.translate[2]]
        rotate = [self.initCamera.rotate[0], self.initCamera.rotate[1], r]
        camera = ObjectPose(translate=translate, rotate=rotate)
        return SceneDescription(camera, self.initAnchor)


    def prepareScenes(self):
        '''
            @see: SceneDescription with the provieded scene
        '''

        alfaCount = self.__getCount(self.generatorDesc.alfa)
        alfaStep = self.generatorDesc.alfa.step
        alfaStart = self.generatorDesc.alfa.start
        result = []
        upTo = int(floor(alfaCount)) + 1
        for i in range(0, upTo):
            alfaValue = i * alfaStep + alfaStart
            print("Alfa:" + str(alfaValue))
            scene = self.__getScene(i, alfaValue)
            result.append(scene)

        return result
