'''
Created on 12-05-2011

@author: Piotr
'''

class SceneDescription(object):
    '''
    @summary: Depicts the scene in the context of the cameras and axis. 
    A quite versatile class should this be.
    
    @attention: this class is not finished or closed yet. 
    '''


    def __init__(self, camera, anchor):
        '''
        Constructor
        @param camera: camera location in the scene passed as @see: ObjectPose
        @param anchor: o
        '''
        self.camera = camera
        self.anchor = anchor
