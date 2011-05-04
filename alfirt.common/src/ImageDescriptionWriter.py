'''
Created on 04-05-2011

@author: Piotr
'''
import unittest

class ImageDescriptionWriter(object):
    '''
    Writes the ImageDescription class to the file stream
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
       
class ImageDescriptionWriterUnitTests(unittest.TestCase):
    def testOutputWithAllElement(self):
        '''
        tests if the output stream is good when parameters passed 
        are good
        '''
        pass
    
    def testOutputWithMissingElement(self):
        '''
        tests if the expeption is raised when some of data is missing
        '''
        pass
        
if (__name__ == 'main'):
    unittest.main()
    
    
        