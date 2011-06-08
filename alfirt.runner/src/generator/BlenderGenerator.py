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
        Constructor. Assumes the file location in the resources file
        render.py
        '''
        self.renderFileLocation = '../render.py'

    def __loadBasis(self):
        '''
        Loads the file shown in the render location
        '''
        pass

    def __injectSceneDescription(self):
        '''
        Injects additional parameters into render script:
            - camera
            - light sources
        '''
        pass

    def __injectFileDescription(self):
        '''
        Injects into render script information about:
            - input file
            - output file
            - resolution
        '''
        pass

    def prepareRender(self, sceneDescription):
        '''
        Prepares the render script for generating.
        @param sceneDescription: description of the scene, mostly involving 
        enviormental settings such as cameras, light sources.
        '''
        pass


#===========================================================================
#  UnitTests
#===========================================================================
class BlenderGeneratorUnitTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_no_file_with_render_basis(self):

        pass

    # TODO: add tests for blender script generator

#===============================================================================
#  Tests runner
#===============================================================================
if (__name__ == 'main'):
    unittest.main(verbosity=2)

