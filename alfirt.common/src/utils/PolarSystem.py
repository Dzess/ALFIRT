'''
Created on 12-05-2011

@author: Piotr
'''

class PolarSystem(object):
    '''
    Transforms from 3D polar system to Cartesian one.
    '''

    def __init__(self):
        '''
        Constructor. Not usable.
        '''

    @classmethod
    def toPolar(cls, x, y, z):
        '''
        Transforms from vector space x,y,z to polar system.
        @param x: x coordinate in vector space
        @param y: y coordinate in vector space
        @param z: z coordinate in vector space   
        
        @attention: Assumes that the center of the polar system vector [0,0,0]
        '''
        return (0, 0, 0)

    @classmethod
    def fromPolar(cls, alfa, beta, radius):
        '''
        Transform from alfa, beta polar space into x,y,z vector space.
        
        @param alfa: angle in degrees [0,360] on the z based space
        @param beta: angle in degrees [0,360] on the x based space
        @param radius: the radius coordinate   
        @attention: Assumes that the center of the polar system vector [0,0,0]
        
        '''
        return (0, 0, 0)
