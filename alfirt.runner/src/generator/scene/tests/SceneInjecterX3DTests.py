'''
Created on Aug 20, 2011

@author: Piotr
'''
import unittest
from generator.scene.SceneInjecterX3D import SceneInjecterX3D
from generator.data.SceneDescription import SceneDescription
from generator.data.ObjectPose import ObjectPose

class TagWriterX3DTests(unittest.TestCase):


    def setUp(self):
        # Setting up the X3D string with ALFIRT namespace tags
        x3dString = """<?xml version="1.0" encoding="UTF-8"?>
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
        self.x3dString = x3dString.replace(" ", "")

        camera = ObjectPose([11, 12, 13], [14, 15, 16])
        anchor = ObjectPose([1, 2, 3], [4, 5, 6])

        self.scene = SceneDescription(camera, anchor)

        # TODO: include the expected version
        expected_x3dString = """<?xml version="1.0" encoding="UTF-8"?>
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
        self.expected_x3dString = expected_x3dString.replace(" ", "")

    def tearDown(self):
        pass


    def testWritingValues(self):
        writer = SceneInjecterX3D()
        resutl = writer.injectScene(data=self.x3dString, scene=self.scene)

        self.assertEqual(resutl, self.expected_x3dString, "The values were not injected")


if __name__ == "__main__":
    unittest.main()
