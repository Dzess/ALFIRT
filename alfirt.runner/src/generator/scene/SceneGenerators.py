'''
Created on Aug 11, 2011

@author: Piotr
'''
import logging

from generator.data.SceneDescription import SceneDescription
from generator.data.ObjectPose import ObjectPose
from math import cos, sin, sqrt, radians, floor

class SceneGeneratorBase(object):
    '''
        Base abstract class for generating scenes
    '''
    def prepareScenes(self):
        raise NotImplementedError("This is abstract method")

class DoubleAxisSceneGenerator(SceneGeneratorBase):
    '''
        Generates @see: SceneDescription objects from @see: GeneratorDescription 
        providing two dimensional rotation in polar system. 
        
        Basing on the alfa angle passed in GeneratorDescription the rotation in horizontal plane
        is done, exactly the same as longitude in geographic. The beta angle specifies the latitude 
        or the vertical rotation in polar system.
        
        The rotations based on alfa and beta angles are completely independent. Meaning that:
        for each step in alfa the all beta positions are computed and generated. The output array of scenes 
        for this algorithm is the network of ALL positions defined by alfa, beta Cartesian product.
        
        @attention: 
            The coordinate system used to pass measure is Absolute (world)  XYZ Euler system.  
    '''
    pass

class SingleAxisSceneGenerator(SceneGeneratorBase):
    '''
        Generates @see: SceneDescription object from the @see: GeneratorDescription object.
        Uses only the alfa  for generation, thus camera moves in the ONE plane - the longitude plane. 
        
        @attention: 
             The coordinate system used to pass measure is Absolute (world)  XYZ Euler system.
    '''
    roundPrecision = 15
    logger = logging.getLogger()

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

        self.logger.info("Scene generator calculated radius: " + str(self.radius))

        self.startingCamera = self.initCamera

        # print out the camera settings
        self.logger.info("Initial camera position: ")
        self.logger.info(str(self.startingCamera))


    def __getCount(self, interval):
        return ((interval.stop - interval.start) / interval.step) if interval.step != 0 else 0


    def __getScene(self, i, alfaValue):

        # translation for circular movement
        x = round(cos(radians(alfaValue)), SingleAxisSceneGenerator.roundPrecision) * self.radius
        y = round(sin(radians(alfaValue)), SingleAxisSceneGenerator.roundPrecision) * self.radius

        # rotation for circular movement
        r = radians(90 + alfaValue)

        # create the translation for the camera
        translate = [x, y, self.startingCamera.translate[2]]
        rotate = [self.startingCamera.rotate[0], self.startingCamera.rotate[1], r]
        camera = ObjectPose(translate=translate, rotate=rotate)

        print("Scene " + str(i) + " with scene object values: ")
        print(camera)

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
        self.logger.info("Preparing %d number of scenes", upTo)
        for i in range(0, upTo):
            alfaValue = i * alfaStep + alfaStart
            self.logger.info("Scene %d rotated with angle %s", i, str(alfaValue))
            scene = self.__getScene(i, alfaValue)
            result.append(scene)

        return result
