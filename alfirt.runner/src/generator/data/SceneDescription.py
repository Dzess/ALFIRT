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
        @param anchor: anchor location in the scene passed as @see: ObjectPose
        '''
        self.camera = camera
        self.anchor = anchor

    def __eq__(self, o):
        if isinstance(o, SceneDescription):
            return o.camera == self.camera and o.anchor == self.anchor

        return False

    def __ne__(self, o):
        return not self == o

    def __str__(self, *args, **kwargs):
        s = "Scene Object: \n"
        s += "Camera:" + str(self.camera) + "\n"
        s += "Anchor:" + str(self.anchor) + "\n"
        return s
