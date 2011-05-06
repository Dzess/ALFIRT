'''
Created on 06-05-2011

@author: Piotr
'''
import unittest

class ArgumentParser(object):
    '''
    Class that specifies how the runner should be worked with. During initializations
    '''


    def __init__(self, arguments):
        '''
        Constructor. Creates the instance of the @see: ArgumentParser
        '''
        if(arguments == None):
            raise ValueError("No None value allowed")
        
        pass

#===============================================================================
# UnitTests
#===============================================================================    
class ArgumentParserUnitTests(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_passing_inncorrect_number_of_values_rises_message(self):
        arguments = []
        with self.assertRaises(ValueError) :
            ArgumentParser(arguments)
    
    def test_passing_no_values_results_in_message(self):
        arguments = None
        # TODO: write checking the message in the exception
        with self.assertRaises(ValueError) :
            ArgumentParser(arguments)
    
#===============================================================================
# Runner for unittest
#===============================================================================
if (__name__ == 'main'):
    unittest.main(verbosity=2)
        