'''
Created on Aug 27, 2011

@author: Piotr
'''
import unittest

class MainTests(unittest.TestCase):
    '''
        End to end tests using the unittest class
    '''

    @unittest.skip(
                   """No sense in making this end to end test working yet. To much
                    dependence on the file system""")
    def test_using_sample_blender_generator(self):

        pass
