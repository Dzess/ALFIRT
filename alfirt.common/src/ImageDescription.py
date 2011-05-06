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
        '''
        self.name = name
        self.x = self.readAxis(x)
        self.y = self.readAxis(y)
        self.z = self.readAxis(z)
        self.p = self.readAxis(p)
        self.q = self.readAxis(q)
        self.r = self.readAxis(r)
        if len(points) % 2 == 1 :
            raise ValueError("The odd number of coordinates is abnormal")
        self.points = points

    def readAxis(self,n):
        '''
        checks if the passed value is within 0-1 range
        @param n: the number whish need to be passed to axis 
        '''
        if (n > 1) or ( n < 0 ):
            raise ValueError("The value of the axis should be within [0..1]")
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
            
        def testtextInsteadOfNumbersOnAxis(self):
            '''
            checks if the passed values of axis are correct (within 0..1)
            '''
            # TODO: get the automation of this process via reflection ? or something like this
            self.x = "some text"
            with self.assertRaises(ValueError) : 
                ImageDescription(self.name,self.x,self.y,self.z,self.p,self.q,self.r,self.points)
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
        
