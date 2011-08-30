'''
Created on Aug 20, 2011

@author: Piotr
'''
import unittest
from generator.scene.SceneInjecterX3D import SceneInjecterX3D
from generator.data.SceneDescription import SceneDescription
from generator.data.ObjectPose import ObjectPose
from lxml import etree
from lxml import objectify

class TagWriterX3DTests(unittest.TestCase):


    def setUp(self):
        self.injecter = SceneInjecterX3D()

        # Setting up the X3D string with ALFIRT namespace tags
        self.x3dString = """<?xml version="1.0" encoding="UTF-8"?>
                        <!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 3.2//EN" "http://www.web3d.org/specifications/x3d-3.2.dtd">
                        <X3D profile="Interchange" version="3.2" 
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

        camera = ObjectPose([0, 0, 0], [0, 0, 0])
        anchor = ObjectPose([1, 2, 3], [4, 5, 6])

        self.scene = SceneDescription(camera, anchor)

        self.expected_x3dString = """<?xml version="1.0" encoding="UTF-8"?>
                        <!DOCTYPE X3D PUBLIC "ISO//Web3D//DTD X3D 3.2//EN" "http://www.web3d.org/specifications/x3d-3.2.dtd">
                        <X3D profile="Interchange" version="3.2" 
                                 xmlns:xsd="http://www.w3.org/2001/XMLSchema-instance"
                                 xmlns:alfirt="ALFIRT" 
                                 xsd:noNamespaceSchemaLocation=" http://www.web3d.org/specifications/x3d-3.2.xsd ">
                            <Scene>
                              <Viewpoint description='Rear View' orientation='-0.9999999403953552 0.0 0.0 1.5707963705062866' position='0.0 0.0 0.0'/> 
                              <Shape alfirt:anchor_translate="0 1 2" alfirt:anchor_rotate="0.4 0.2 0.3">
                                <IndexedFaceSet coordIndex="0 1 2">
                                  <Coordinate point="0 0 0 1 0 0 0.5 1 0"/>
                                </IndexedFaceSet>
                              </Shape>
                            </Scene>
                        </X3D>
        """


    def test_writing_proper_values(self):

        result = self.injecter.injectScene(data=self.x3dString, scene=self.scene)

        print(result)

        # get the whitespace trimmed
        expected_tree = objectify.fromstring(self.expected_x3dString.encode(encoding='ascii', errors='ignore'))
        result_tree = objectify.fromstring(result.encode(encoding='utf_8', errors='strict'))

        expected_string = etree.tostring(expected_tree)
        result_string = etree.tostring(result_tree)

        print(expected_string)
        print(result_string)

        self.assertEqual(result_string, expected_string, "The values were not injected")

    def test_writing_nones_values(self):

        with self.assertRaises(TypeError):
            self.injecter.injectScene(None, None)

    def test_writing_wrong_values(self):

        with self.assertRaises(TypeError):
            self.injecter.injectScene(3, "scene")

if __name__ == "__main__":
    unittest.main()
