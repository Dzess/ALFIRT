'''
Created on 04-05-2011

@author: Piotr
'''

class ImageDescription(object):
    '''
    Class represents the image characteristics from the 
    learning point of view.
    
    Consists of fields:
    element name - name of the file which this descriptions
    
    '''

    def __init__(self, name, x, y, z,
                  p, q, r, points):
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

    def validate(self, n):
        '''
        Checks if the passed value is number
        @param n: the number which need to be passed to axis 
        '''
        if not isinstance(n, (float, int)) :
            raise ValueError("The value passed should be number")
        return n

    def __eq__(self, o):
        if not isinstance(o, self.__class__) :
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
        string = "Name: " + str(self.name) + "\n"
        string += "X: " + str(self.x) + "\n"
        string += "Y: " + str(self.y) + "\n"
        string += "Z: " + str(self.z) + "\n"
        string += "P: " + str(self.p) + "\n"
        string += "Q: " + str(self.q) + "\n"
        string += "R: " + str(self.r) + "\n"
        string += self.getPoints()
        return  string
