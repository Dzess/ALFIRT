'''
Created on 10-05-2011

@author: Piotr
'''
import unittest
import os

from xml.dom import minidom
import xpath

from generator.SceneDescription import SceneDescription
from generator.ObjectPose import ObjectPose



class TagReaderX3D(object):
    '''
    Reads the data stream gets the ALFIRT tags from XML document. 
    '''


    def __init__(self):
        '''
        Constructor
        '''


    def __getCameraElement(self, xmldoc):
        elements = xmldoc.getElementsByTagName('Viewpoint')

        # Get the first one element from Viewpoint (usually there should be one)
        element = elements[0]

        print "\n"
        print element.toxml()
        orientation = element.attributes['orientation']
        position = element.attributes['position']

        # Split string by ' ' and get the values
        orientations = orientation.value.split(' ')
        positions = position.value.split(' ')

        translate = []
        translate.append(float(positions[0]))
        translate.append(float(positions[1]))
        translate.append(float(positions[2]))

        rotate = []
        rotate.append(float(orientations[0]))
        rotate.append(float(orientations[1]))
        rotate.append(float(orientations[2]))

        return ObjectPose(translate, rotate)

    def __traverseDomTree(self, node, xmldoc, attribute):
        for subelement in xmldoc.getElementsByTagName(node):
            print help(subelement)
            if subelement.hasAttribute(attribute):
                return subelement
            else:
                return self.__traverseDomTree(subelement, xmldoc, attribute)
        return None

    def __getAnchorElement(self, xmldoc):

        # Start finding the element about translation and rotation
        # find only the fist element
        rootNode = xmldoc.getElementsByTagName("Scene")[0]
        context = xpath.XPathContext()
        context.namespaces['prefix'] = "ALFIRT"
        anchor_t_node = context.findnode("//*[@prefix:anchor_translate]", rootNode)

        anchor_r_node = context.findnode("//*[@prefix:anchor_rotate]", rootNode)


        # Read the values from selected nodes

        translations = anchor_t_node.attributes['alfirt:anchor_translate'].value.split(' ')

        rotation = anchor_r_node.attributes['alfirt:anchor_rotate']
        rotations = rotation.value.split(' ')

        translate = []
        rotate = []

        translate.append(float(translations[0]))
        translate.append(float(translations[1]))
        translate.append(float(translations[2]))

        rotate.append(float(rotations[0]))
        rotate.append(float(rotations[1]))
        rotate.append(float(rotations[2]))

        return ObjectPose(translate, rotate)


    def readFile(self, file):
        '''
        Reads file in .x3d format and returns the data from ALFIRT tags
        '''
        if (file == None) :
            raise ValueError("The file attribute is mandatory")

        if not os.path.exists(file):
            raise ValueError("The file provided does not exists")

        # using XML broad available library read file
        xmldoc = minidom.parse(file)

        # Get the anchor element
        anchor = self.__getAnchorElement(xmldoc)

        # Get the camera element
        camera = self.__getCameraElement(xmldoc)

        result = SceneDescription(anchor=anchor, camera=camera)

        return result

#===============================================================================
#  UnitTests
#===============================================================================
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

    def test_reading_file_with_no_anchor_results_in_exception(self):
        '''
            The anchor is required for the polar transformations around the object.
        '''
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

        self.assertEqual(translateAnchor, [0.0, 1.0, 2.0], 'Translate of the anchor should be 0 1 2')
        self.assertEqual(rotateAnchor , [0.4, 0.2, 0.3 ], "Rotate of the anchor should be 0.4, 0.2 0.3")

        self.assertEqual(translateCamera, [0.0, 0.0, -10.0], "The position of the camera should be 0 0 -10")
        self.assertEqual(rotateCamera, [0.0, 1.0, 0.0], "The rotation of the camera should be 0 1 0 3.14")

        pass

#===============================================================================
#  Test runner
#===============================================================================
if (__name__ == 'main'):
    unittest.main(verbosity=2)

