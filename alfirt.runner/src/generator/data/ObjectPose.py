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
        '''
        self.translate = translate
        self.rotate = rotate

    def __str__(self):
        '''
        To String method. Prints all the values from rotation and translation
        '''
        string = "Translation: " + self.translate + '\n'
        string += "Rotation: " + self.rotate + '\n'
        return string

