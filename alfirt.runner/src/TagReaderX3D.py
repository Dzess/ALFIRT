'''
Created on 10-05-2011

@author: Piotr
'''
import unittest

class TagReaderX3D(object):
    '''
    Reads the data stream gets the ALFIRT tags from XML document. 
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
#===============================================================================
#  UnitTests
#===============================================================================
class TagReaderX3DUnitTests(unittest.TestCase):
    
    
    def setUp(self):
        pass
    
    def testDown(self):
        pass

    # TODO: add tests here for x3d namespace finding in X3D file format

#===============================================================================
#  Test runner
#===============================================================================
if (__name__ == 'main'):
    unittest.main(verbosity=2)