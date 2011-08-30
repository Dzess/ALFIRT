'''
Created on Jun 9, 2011

@author: Piotr
'''
import unittest
import os

from readers.TagReaderX3D import TagReaderX3D

class TagReaderX3DUnitTests(unittest.TestCase):


    def setUp(self):

        # Setting up the X3D string with ALFIRT namespace tags
        x3dString = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 3.2//EN" "http://www.web3d.org/specifications/x3d-3.2.dtd">
 
<X3D profile="Interchange" 
version="3.2" 
xmlns:xsd="http://www.w3.org/2001/XMLSchema-instance"
xmlns:alfirt="ALFIRT" 
xsd:noNamespaceSchemaLocation=" http://www.web3d.org/specifications/x3d-3.2.xsd ">
<Scene>
  <Viewpoint description='Rear View' orientation='0 1 0 3.14159' position='0 0 -10'/> 
  <Shape alfirt:anchor_translate="0 1 2" alfirt:anchor_rotate="0.4 0.2 0.3">
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

    def tearDown(self):
        # Removing file after test
        os.remove(self.fileName)

    def test_reading_none_results_in_exception(self):

        x3dReader = TagReaderX3D()
        with self.assertRaises(ValueError):
            x3dReader.readScene(None)

        with self.assertRaises(ValueError):
            x3dReader.readScene("some no existing file")

    def test_reading_file_with_no_anchor_results_in_exception(self):
        '''
            The anchor is required for the polar transformations around the object.
        '''
        # Setting up the X3D string with ALFIRT namespace tags
        x3dString = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 3.2//EN" "http://www.web3d.org/specifications/x3d-3.2.dtd">
 
<X3D profile="Interchange" 
version="3.2" 
xmlns:xsd="http://www.w3.org/2001/XMLSchema-instance"
xmlns:alfirt="ALFIRT" 
xsd:noNamespaceSchemaLocation=" http://www.web3d.org/specifications/x3d-3.2.xsd ">
<Scene>
  <Viewpoint description='Rear View' orientation='0 1 0 3.14159' position='0 0 -10'/> 
  <Shape>
    <IndexedFaceSet coordIndex="0 1 2">
      <Coordinate point="0 0 0 1 0 0 0.5 1 0"/>
    </IndexedFaceSet>
  </Shape>
</Scene>
</X3D>
        """
        # Write this file into the data
        fileName = "test_file_without_anchor"
        with open(fileName, 'w') as fileStream:
            fileStream.write(x3dString)
            fileStream.close()

        # Get reader
        x3dReader = TagReaderX3D()
        try:
            x3dReader.readScene(fileName)
        except RuntimeError:
            return
        finally:
            os.remove(fileName)

        self.fail("The exception should have been thrown")


    def test_reading_file_with_alfirt_tags(self):
        '''
            Checks if the elements passed in X3D string are correct.
        '''
        x3dReader = TagReaderX3D()
        results = x3dReader.readScene(self.fileName)

        # assert the values
        translateCamera = results.camera.translate
        rotateCamera = results.camera.rotate

        translateAnchor = results.anchor.translate
        rotateAnchor = results.anchor.rotate

        self.assertEqual(translateAnchor, [0.0, 1.0, 2.0], 'Translate of the anchor should be 0 1 2')
        self.assertEqual(rotateAnchor , [0.4, 0.2, 0.3 ], "Rotate of the anchor should be 0.4, 0.2 0.3")

        self.assertEqual(translateCamera, [0.0, -10, 0], "The position of the camera should be 0 0 -10")
        self.assertEqual(rotateCamera, [1.5707963705062866, 1.7340079025429667e-13, 3.1415903568267822], "The rotation of the camera should be 0 1 0 3.14")

#===============================================================================
#  Test runner
#===============================================================================
if (__name__ == 'main'):
    unittest.main(verbosity=2)


