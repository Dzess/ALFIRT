'''
Created on Sep 5, 2011

@author: Piotr
'''
from mockito.mocking import mock
from math import sqrt
from generator.data.GeneratorInterval import GeneratorInterval
from generator.data.ObjectPose import ObjectPose

class SceneGeneratorTestsBase(object):
    '''
        Helper class for wiring tests for image SceneGenerators 
    '''

    def getDifferMessage(self, expected, actual):
        '''
            Gets the message about different scenes.
        '''
        string = "Scene differs: expected:" + str(expected) + "\n"
        string += "but got " + str(actual) + "\n"
        return  string

    def getGeneratorDescription(self, alfa, beta, translate):
        '''
            Gets the generator description with already set radius. 
            Ready for injection of alfa and beta.
        '''

        generatorDesc = mock(mocked_obj=None, strict=True)

        # TODO: make this code more usable
        #radius_sqrt = sqrt(25 + 25)
        radius_sqrt = sqrt(translate[0]*translate[0] + translate[2]*translate[2])
        radius_sqrt = sqrt(radius_sqrt * radius_sqrt + translate[1]*translate[1])

        radius = GeneratorInterval(start=radius_sqrt, stop=radius_sqrt)
        generatorDesc.alfa = alfa
        generatorDesc.beta = beta
        generatorDesc.radius = radius

        return generatorDesc

    def getInitAnchor(self):
        '''
            Gets anchor ObjectPose with 0 on all values. Meaning that 
            object is inside the coordinate system.
        '''
        return ObjectPose([0, 0, 0], [0, 0, 0])
