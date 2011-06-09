'''
Created on 10-05-2011

@author: Piotr
'''
import os

from xml.dom import minidom
import xpath

from generator.SceneDescription import SceneDescription
from generator.ObjectPose import ObjectPose



class TagReaderX3D(object):
    '''
    Reads the data stream gets the ALFIRT tags from XML document. 
    '''

    namespace = "ALFIRT"

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
        context.namespaces['prefix'] = TagReaderX3D.namespace
        anchor_t_node = context.findnode("//*[@prefix:anchor_translate]", rootNode)

        anchor_r_node = context.findnode("//*[@prefix:anchor_rotate]", rootNode)

        # No anchor element found which is mandatory
        if (anchor_r_node == None) or (anchor_t_node == None):
            raise ValueError("No anchor element found in the file")

        # Read the values from selected nodes
        translations = anchor_t_node.getAttributeNS(TagReaderX3D.namespace, "anchor_translate").split(' ')
        rotations = anchor_r_node.getAttributeNS(TagReaderX3D.namespace, "anchor_rotate").split(' ')


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
        Reads file in .x3d format and returns the data from ALFRT tags.
        @param file: the path to the .x3d file tagged with ALFIRT attributes. 
        @return: the @see: SceneDescription object with anchor. Camera object is optional.
        
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

