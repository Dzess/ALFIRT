'''
Created on 10-05-2011

@author: Piotr
'''
import unittest

class BlenderGenerator(object):
    '''
    Generates the .py file for rendering complaint with blender 2.57.
    '''


    def __init__(self):
        '''
        Constructor. 
        '''
    
#===========================================================================
#  UnitTests
#===========================================================================
class BlenderGeneratorUnitTests(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    # TODO: add tests for blender script generator
    
#===============================================================================
#  Tests runner
#===============================================================================
if (__name__ == 'main'):
    unittest.main(verbosity=2)