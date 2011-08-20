'''
Created on Aug 20, 2011

@author: Piotr
'''

class SceneInjecterBase(object):
    """
        Abstract class for Scene Injecter
    """

    def injectScene(self, data, scene):
        raise NotImplementedError("This is abstract method")


class SceneInjecterX3D(SceneInjecterBase):
    '''
    Writer class for .x3d files.
    Allowing injecting various value into existing 
    file. 
    '''


    def __init__(self):
        '''
        Constructor
        '''

    def injectScene(self, data, scene):
        '''
        Injects into the specified file scene description values
        @param scene: Object of class @see: SceneDescription
        @param data: String with the data (x3d) in case of this class to be 
        injected into 
        '''
        pass
