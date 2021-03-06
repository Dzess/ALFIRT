'''
Created on Sep 9, 2011

@author: Ankhazam & Piotr & OpenCV team
'''
from algorithms.AlgorithmBase import AlgorithmBase
import classification.ORBFlannMatcher as OFM
import classification.TrainedObject as TO
import image.ImageDescriptionReader as IDR
import image.ImageDescriptionWriter as IDW
import common.Utils as TU
import cv2
import os
import shutil

class ORBFlannMatchingAlgorithm(AlgorithmBase):
    '''
        New algorithm used for matching orientations using Flann matching method.
    '''
    

    def __init__(self):
        '''
            Constructor
        '''
        self.detector = cv2.FastFeatureDetector(16, True)
        self.detector = cv2.GridAdaptedFeatureDetector(self.detector)
        self.extractor = cv2.DescriptorExtractor_create('ORB')


    def __train(self, learningPath):
        '''
            Trains the system with new object data
            
            @param learningPath: Has to be root of the following structure
            
            learningPath
                |_ObjectA
                |    |_1.imd, 1.ren
                |    |_...
                |_ObjectB
                |    |_...
                |_ObjectC
                     |_...
            
            @return: List of @see: TrainedObject
        '''

        trainedObjects = list() # list of trained objects

        for (root, dirs, files) in os.walk(learningPath):
            if len(dirs) == 0: # we're in an object folder

                # ObjectFilename
                objName = os.path.basename(root)
                print "root: ", objName

                # currently trained object
                trainedObject = TO.TrainedObject(objName, 0)

                # real training
                for file1 in files: # we won't implement natural human sorting

                    # do not use .* and *.imd files
                    if file1.startswith('.') or file1.endswith(".imd"):
                        continue

                    # fetching ImageDescription
                    imDescPath = os.path.join(root, file1[:-4]) + ".imd"
                    print "imd: ", imDescPath
                    with open(imDescPath, 'r') as imDF:
                        # read this file using reader
                        reader = IDR.ImageDescriptionReader()
                        imageDesc = reader.read(imDF)

                    # fetching relevant SURF features
                    imagePath = os.path.join(root, file1)
                    image = cv2.imread(imagePath)
                    keypoints = self.detector.detect(image)
                    keypoints, descriptors = self.extractor.compute(image,keypoints)                    

                    # adding orientation to trainedObject
                    trainedObject.addOrientation(0, (imageDesc, keypoints, descriptors, imagePath))

                # once trained all orientations we can add the object to the DBase
                trainedObjects.append(trainedObject)

        return trainedObjects

    def learn(self, inputFolder):
        self.trainedObjects = self.__train(inputFolder)

    def test(self, inputFolder, outputFolder):


        imageDescWriter = IDW.ImageDescriptionWriter()

        for file1 in os.listdir(inputFolder):

            # do not use .* files
            if file1.startswith("."):
                continue

            # save output (the name of the object without .bmp / .jpg etc)
            fileName = os.path.basename(file1)
            fileName = os.path.splitext(fileName)[0]
            imgOutPath = os.path.join(outputFolder, fileName)
            if not os.path.exists(imgOutPath):
                os.mkdir(imgOutPath)

            # with image files do ...
            if not file1.endswith(".imd"):

                # flags are set to 0 = meaning grey scale
                testImage = cv2.imread(os.path.join(inputFolder, file1), flags=0)
                kp = self.detector.detect(testImage)
                kp, desc = self.extractor.compute(testImage,kp)                     
                print "Loaded test image : '%s'" % file1

                kpImage = cv2.imread(os.path.join(inputFolder, file1))
                cvUtilities = TU.Utils(0)
                cvUtilities.drawKeypoints(kpImage, kp, color=(255, 255, 0))
                cv2.imwrite(os.path.join(outputFolder, file1), kpImage)

                matcher = OFM.ORBFlannMatcher(self.trainedObjects)
                match = matcher.matchObject(testImage)
                print "Finished processing file '%s'" % file1

                for obj in match:
                    print "Object Name: ", obj[0].name
                    print "OrientationName: ", obj[0].orientations[obj[1]][0].name
                    with open(os.path.join(imgOutPath, "computed") + ".imd", 'w') as fileStream:
                        imageDescWriter.write(fileStream, obj[0].orientations[obj[1]][0])

                    matchedPath = obj[0].orientations[obj[1]][3]

                    #show the match
                    matchedImage = cv2.imread(matchedPath, cv2.IMREAD_GRAYSCALE)
                    vis = cvUtilities.draw_match(matchedImage, testImage, obj[4][0], obj[4][1], obj[2], obj[3])

                    # show image
                    cv2.imshow("match!", vis)
                    cv2.waitKey()

            # with .imd files to this
            else :
                src = os.path.join(inputFolder, file1)
                dst = os.path.join(imgOutPath, "expected.imd")
                print "Coping the file '%s' into '%s'" % (src, dst)
                shutil.copyfile(src, dst)

