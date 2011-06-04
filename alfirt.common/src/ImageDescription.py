'''
Created on 04-05-2011

@author: Piotr
'''
import unittest

class ImageDescription(object):
    '''
    Class represents the image characteristics from the 
    learning point of view. 
    '''
    
    def __init__(self,name, x,  y,  z,
                  p,  q,  r, points):
        '''
        Constructor. Creates the immutable object of the image values with
        passed arguments.
        @param name: the name of the image
        @param x: x coordinate in translation vector
        @param y: y coordinate in translation vector
        @param z: z coordinate in translation vector
        
        TODO: add better description of latter elements
        '''
        self.name = name
        self.x = self.validate(x)
        self.y = self.validate(y)
        self.z = self.validate(z)
        self.p = self.validate(p)
        self.q = self.validate(q)
        self.r = self.validate(r)
        if len(points) % 2 == 1 :
            raise ValueError("The odd number of coordinates is abnormal")
        self.points = points

    def validate(self,n):
        '''
        Checks if the passed value is number
        @param n: the number which need to be passed to axis 
        '''
        if not isinstance(n,(float,int,long)) :
            raise ValueError("The value passed should be number")
        return n
        
    def __eq__(self, o):
        if not isinstance(o,self.__class__) :
            return False
        return self.x == o.x and self.y == o.y and self.z == o.z and self.p == o.p and self.q == o.q and self.r == o.r and self.name == o.name and self.points == o.points
    
    def __ne__(self, o):
        return not self == o
    
    def getPoints(self):
        '''
        Returns the string with the points
        '''
        points = "Points: \n"
        for point in self.points:
            points += str(point) + " "
        points += '\n'
        return points
    
    def __repr__(self):
        string  = "Name: " + str(self.name) + "\n" 
        string += "X: " + str(self.x) + "\n"
        string += "Y: " + str(self.y) + "\n"
        string += "Z: " + str(self.z) + "\n"
        string += "P: " + str(self.p) + "\n"
        string += "Q: " + str(self.q) + "\n"
        string += "R: " + str(self.r) + "\n"
        string += self.getPoints()
        return  string
        
        
class ImageDescriptionUnitTests(unittest.TestCase):
        def setUp(self):                
            # set up example data
            self.name = "sample_image"
            self.x = 0
            self.y = 0.5
            self.z = 0.75
            self.p = 0
            self.q = 0.25
            self.r = 0.85
            self.points = [0.0, 1.0, 2.0, 3.0]
        
        def testEqualityOnAllProperties(self):
            '''
            tests the equality comparer
            '''
            imag1 = ImageDescription(self.name,self.x,self.y,self.z,self.p,self.q,self.r,self.points)
            imag2 = ImageDescription(self.name,self.x,self.y,self.z,self.p,self.q,self.r,self.points)
            
            self.assertEqual(imag1, imag2, "The images are equal")
            pass
        
        def testEqualityComparisionOnPoints(self):
            '''
            checks if the points are used for comparison
            '''
            points2 = [0.0, 2.0]
            imag1 = ImageDescription(self.name,self.x,self.y,self.z,self.p,self.q,self.r,self.points)
            imag2 = ImageDescription(self.name,self.x,self.y,self.z,self.p,self.q,self.r,points2)
            
            self.assertNotEqual(imag1, imag2, "Image description are different because of the mask")
            pass
            
        def testNotSameInstanceBeingCompared(self):
            '''
            check if passing some other object and ImageDescription results in nice False message
            '''
            imag1 = ImageDescription(self.name,self.x,self.y,self.z,self.p,self.q,self.r,self.points)
            imag2 = [2.0,3.0]
            self.assertNotEqual(imag1, imag2, "Thie values should not be equal, nor exception should be thrown") 
            pass
        
        def testAllAxisArgumentsMustBeANumber(self):
            '''
            checks if the values provided within the axis parameters are numbers
            '''
            value = "some_text_which_is_not_a_number"
            numberParameters = [ 'x', 'y', 'z','p','q','r']
            for index in range(0,len(numberParameters)):
                args = [self.name,self.x,self.y,self.z,self.p,self.q,self.r,self.points]
                # manipulate argument list to get the specified pa
                args[index+1] = value
                with self.assertRaises(ValueError) : 
                    ImageDescription(*args)    
                pass
            pass
        
        def testOutputWithOddNumberOfPonts(self):
            '''
            should raise an error when the number of points passed to the image is odd
            '''
            # odd number of points
            self.points = [1.0, 2.0, 3.0]
            
            with self.assertRaises(ValueError) :
                ImageDescription(self.name,self.x,self.y,self.z,self.p,self.q,self.r,self.points)
                 
            pass
        def testNormalDataShouldGoWithoutProblem(self):
            '''
            tests if the normal data passes the constructor
            '''
            ImageDescription(self.name,self.x,self.y,self.z,
                            self.p,self.q,self.r,self.points)
            pass
        
if (__name__ == 'main'):
    unittest.main(verbosity=2)