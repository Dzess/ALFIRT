'''
Created on Jun 6, 2011

@author: Piotr
'''

class ObjectPose(object):
    '''
    Represents the position and orientation of the object in the
    Cartesian coordinate system.
    '''


    def __init__(self, translate, rotate):
        '''
        Constructor
        @param translate: list with translation parameters in x,y,z coordinate system
        @param rotate: list with rotation parameters in x,y,z coordinate system 
        @attention: rotation elements MUST BE IN RADIANS
        '''
        self.translate = translate
        self.rotate = rotate

    def __str__(self):
        string = "Translation: " + str(self.translate) + '\n'
        string += "Rotation: " + str(self.rotate) + '\n'
        return string

    def __eq__(self, o):
        if isinstance(o, ObjectPose):
            return self.translate == o.translate and self.rotate == o.rotate

        return False

    def __ne__(self, o):
        return not self == o
