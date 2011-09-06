'''
Created on 05-05-2011

@author: Ankhazam
'''

from optparse import OptionParser
import sys
import os
import classification.FlannMatcher as FM
import classification.TrainedObject as TO
import image.ImageDescriptionReader as IDR
import cv2
import utils.Utils as TU



def train(learningPath, threshold=400):
    '''
    Trains the system with new object data
    
    @param learningPath: Has to be root of the following structure
    @param threshold: SURF Hessian threshold used for training 
    
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
    
    trainingUtils = TU.Utils(threshold)
    
    for (root, dirs, files) in os.walk(learningPath):
        if len(dirs) == 0: # we're in an object folder
            
            # ObjectFilename
            objName = os.path.basename(root) 
            print "root: ", objName
            
            # currently trained object
            trainedObject = TO.TrainedObject(objName,threshold)
            
            # orientation list cleanup
            orientationNames = list()
            for file1 in files:
                orientationNames.append(file1[:-4])
            
            # real training
            for file1 in set(orientationNames): # we won't implement natural human sorting
                
                # fetching ImageDescription
                imDescPath = os.path.join(root, file1)+".imd"
                print "imd: ", imDescPath
                with open(imDescPath, 'r') as imDF:
                    # read this file using reader
                    reader = IDR.ImageDescriptionReader()
                    imageDesc = reader.read(imDF)
                
                # fetching relevant SURF features
                imagePath = os.path.join(root, file1)+".bmp" # TODO: Multiple image types!!!
                image = cv2.imread(imagePath)
                (keypoints, descriptors) = trainingUtils.findSURF(image, threshold)
                
                # adding orientation to trainedObject
                trainedObject.addOrientation(threshold, (imageDesc,keypoints,descriptors))
                
            # once trained all orientations we can add the object to the DBase
            trainedObjects.append(trainedObject)
            
    return trainedObjects
                

if __name__ == '__main__':
    print "Matcher Learning and Testing Application"
    
    parser = OptionParser(usage="usage: %prog [options] [learning_files_path/dbase_file_path] [test_files_path] [results_path]")
    parser.add_option("-r", "--runType", action="store", dest="runType", type="str",
        help="Run selection learn|test|full. \"learn\" requires 1st path, \"test\"  2nd and 3rd, \"full\" all three of them.",
        default="test")
    parser.add_option("-t", "--threshold", action="store", dest="threshold", type="int", 
                      help="SURF Hessian threshold used for training.",default="400")
    (options, args) = parser.parse_args()
    
    learnPath, testPath, outPath = None, None, None
    
    if ((options.runType != "learn") & (options.runType != "test") & (options.runType != "full")):
        print "Invalid argument for -r option: " + options.runType
        sys.exit()
    
    elif (options.runType == "learn"):
        if len(args) < 1:
            print "Required path to directory with learning files missing."
            sys.exit()
        print "Learning mode"
        learnPath = args[0]
        
        train(learnPath,options.threshold) #TODO: Add saving of the DBASE

        print "done learning"
    
    elif (options.runType == "test"):
        if len(args) < 3:
            print "Missing some of the required paths (need path_to_trainedDBase, testing_images_directory and output_directory)."
            sys.exit()
        print "Testing mode"
        testPath = args[0]
        outPath = args[1]
        
        raise NotImplementedError("To be added")
    
    elif  (options.runType == "full"):
        if len(args) < 3:
            print "Missing some of the required paths."
            sys.exit()
        print "Learning followed by Testing mode."
        learnPath = args[0]
        testPath = args[1]
        outPath = args[2]

        trainedObjects = train(learnPath,options.threshold)
        cvUtilities = TU.Utils(options.threshold)
        
        bestMatches = list()
        for file1 in os.listdir(args[1]):
            testImage = cv2.imread(os.path.join(args[1],file1), cv2.IMREAD_GRAYSCALE)
            matcher = FM.FlannMatcher(trainedObjects, options.threshold)
            bestMatches.append(matcher.matchObject(testImage))
            
        # TODO: do something with the found bestMatches ;)
        print "done full"