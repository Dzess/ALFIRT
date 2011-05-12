'''
Created on 10-05-2011

@author: Piotr
'''
import unittest
import os

class TagReaderX3D(object):
    '''
    Reads the data stream gets the ALFIRT tags from XML document. 
    '''


    def __init__(self):
        '''
        Constructor
        '''

    def readFile(self, file):
        '''
        Reads file in .x3d format and returns the data from ALFIRT tags
        '''
        if (file == None) :
            raise ValueError("The file attribute is mandatory")

        if not os.path.exists(file):
            raise ValueError("The file provided does not exists")

        # TODO: write this using xml broad avaliable library
        # Read file

        # Get the anchor element

        # Get the camera element
        pass

#===============================================================================
#  UnitTests
#===============================================================================
class TagReaderX3DUnitTests(unittest.TestCase):


    def setUp(self):

        # Setting up the X3D string with ALFIRT namespace tags
        x3dString = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 3.2//EN" "http://www.web3d.org/specifications/x3d-3.2.dtd">
 
<X3D profile="Interchange" 
version="3.2" 
xmlns:xsd="http://www.w3.org/2001/XMLSchema-instance"
xmlns:alfirt="ALFIRT" 
xsd:noNamespaceSchemaLocation=" http://www.web3d.org/specifications/x3d-3.2.xsd ">
<Scene>
  <Viewpoint description='Rear View' orientation='0 1 0 3.14159' position='0 0 -10'/> 
  <Shape alfirt:anchor="0 1 2 0.4 0.2 0.3">
    <IndexedFaceSet coordIndex="0 1 2">
      <Coordinate point="0 0 0 1 0 0 0.5 1 0"/>
    </IndexedFaceSet>
  </Shape>
</Scene>
</X3D>
        """
        # Creating file
        self.fileName = "test_file_name"
        with open(self.fileName, 'w') as fileStream:
            fileStream.write(x3dString)
            fileStream.close()
        pass

    def tearDown(self):
        # Removing file after test
        os.remove(self.fileName)
        pass

    def test_reading_none_results_in_exception(self):

        x3dReader = TagReaderX3D()
        with self.assertRaises(ValueError):
            x3dReader.readFile(None)

        with self.assertRaises(ValueError):
            x3dReader.readFile("some no existing file")
        pass

    def test_reading_file_with_alfirt_tags(self):
        '''
        Checks if the elements passed in X3D string are correct.
        '''
        x3dReader = TagReaderX3D()
        results = x3dReader.readFile(self.fileName)

        # assert the values
        translateCamera = results.camera.translate
        rotateCamera = results.camera.rotate

        translateAnchor = results.anchor.translate
        rotateAnchor = results.anchor.rotate

        self.assertEqual(translateAnchor, [0, 1, 2], 'Translate of the anchor should be 0 1 2')
        self.assertEqual(rotateAnchor , [0.4, 0.2, 0.3 ], "Rotate of the anchor should be 0.4, 0.2 0.3")

        self.assertEqual(translateCamera, [0, 0, -10], "The position of the camera should be 0 0 -10")
        self.assertEqual(rotateCamera, [0, 1, 0], "The rotation of the camera should be 0 1 0 3.14")

        pass

#===============================================================================
#  Test runner
#===============================================================================
if (__name__ == 'main'):
    unittest.main(verbosity=2)
