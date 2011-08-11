'''
Created on Aug 11, 2011

@author: Piotr
'''
from generator.data.SceneDescription import SceneDescription

class SceneGenerator(object):
    '''
    Generates @see: SceneDescription object from the @see: GeneratorDescription object.
    '''


    def __init__(self, generatorDesc):
        '''
        Constructor.
        @param generatorDesc: instance of the @see: GeneratorDescription class.
        '''
        self.generatorDesc = generatorDesc


    def __getCount(self, interval):
        return ((interval.stop - interval.start) / interval.step) if interval.step != 0 else 0


    def prepareScenes(self):
        '''
            Gets the list of @see: SceneDescription with the provieded scene
        '''
        alfaCount = self.__getCount(self.generatorDesc.alfa)
        betaCount = self.__getCount(self.generatorDesc.beta)
        radiusCount = self.__getCount(self.generatorDesc.radius)

        result = []
        for i in range(0, alfaCount + 1):
            result.append(SceneDescription(None, None))
        print len(result)
        return result


