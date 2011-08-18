'''
Created on 04-05-2011

@author: Piotr Jessa
'''


from image.ImageDescription import ImageDescription

class ImageDescriptionWriter(object):
    '''
    Writes the ImageDescription class to the file stream
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass

    def writeline(self, text):
        '''
        writes the text ended with \n to the stream
        '''
        self.stream.write(text)
        self.stream.write('\n')

    def write(self, stream, imageDescription):
        '''
        writes the image description formatted into stream
        '''
        self.stream = stream

        self.writeline("@name")
        self.writeline(imageDescription.name)

        self.writeline("@translate")
        self.writeline(str(imageDescription.x))
        self.writeline(str(imageDescription.y))
        self.writeline(str(imageDescription.z))

        self.writeline("@rotate")
        self.writeline(str(imageDescription.p))
        self.writeline(str(imageDescription.q))
        self.writeline(str(imageDescription.r))

        self.writeline("@data")
        self.writeline(str(len(imageDescription.points) / 2))
        for i in range(1, len(imageDescription.points), 2):
            stream.write(str(imageDescription.points[i - 1]))
            stream.write(' ')
            self.writeline(str(imageDescription.points[i]))
