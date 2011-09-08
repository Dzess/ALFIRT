'''
Created on 05-05-2011

@author: Ankhazam & Dzess

'''

from optparse import OptionParser
import sys
import os
import shutil

def pathSetUp():
    print "Setting up internal paths to PYTHONPATH"

    commonsPathSetUp()
    # NOTE: add here elements to be used

def commonsPathSetUp():
    commonNames = os.path.join(__file__, "..", "..", "..", "alfirt.common", "src")
    commonsPath = os.path.abspath(commonNames)

    print "Appending '%s' " % commonsPath
    sys.path.append(commonsPath)

def getParser():
    parser = OptionParser(usage="usage: %prog [options] [learning_files_path/dbase_file_path] [test_files_path] [results_path]")
    parser.add_option("-r", "--runType", action="store", dest="runType", type="str", help="Run selection learn|test|full. \"learn\" requires 1st path, \"test\"  2nd and 3rd, \"full\" all three of them.", default="test")
    parser.add_option("-t", "--threshold", action="store", dest="threshold", type="int", help="SURF Hessian threshold used for training.", default="400")
    options, args = parser.parse_args()
    return options, args


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
            trainedObject = TO.TrainedObject(objName, threshold)

            # orientation list cleanup
            orientationNames = list()
            for file1 in files:
                orientationNames.append(file1[:-4])

            # real training
            for file1 in set(orientationNames): # we won't implement natural human sorting

                # do not use .* files
                if file1.startswith('.'):
                    continue

                # fetching ImageDescription
                imDescPath = os.path.join(root, file1) + ".imd"
                print "imd: ", imDescPath
                with open(imDescPath, 'r') as imDF:
                    # read this file using reader
                    reader = IDR.ImageDescriptionReader()
                    imageDesc = reader.read(imDF)

                # fetching relevant SURF features
                imagePath = os.path.join(root, file1) + ".bmp" # TODO: Multiple image types!!!
                image = cv2.imread(imagePath)
                (keypoints, descriptors) = trainingUtils.findSURF(image, threshold)

                # adding orientation to trainedObject
                trainedObject.addOrientation(threshold, (imageDesc, keypoints, descriptors))

            # once trained all orientations we can add the object to the DBase
            trainedObjects.append(trainedObject)

    return trainedObjects


if __name__ == '__main__':
    print "Matcher Learning and Testing Application"

    # set up all the paths
    pathSetUp()

    # proceed with imports
    try:
        import classification.FlannMatcher as FM
        import classification.TrainedObject as TO
        import image.ImageDescriptionReader as IDR
        import image.ImageDescriptionWriter as IDW
        import cv2
        import utils.Utils as TU
    except ImportError as ie:
        print "Importing not successful"
        print ie
        sys.exit(1)

    # configure the parser and reparse the options
    options, args = getParser()
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

        train(learnPath, options.threshold) #TODO: Add saving of the DBASE

        print "done learning, however forgot the knowledge... therefore"
        raise NotImplementedError("Needs adding knowledge saving")

    elif (options.runType == "test"):
        if len(args) < 3:
            print "Missing some of the required paths (need path_to_trainedDBase, testing_images_directory and output_directory)."
            sys.exit()
        print "Testing mode"
        testPath = args[0]
        outPath = args[1]

        raise NotImplementedError("Needs adding knowledge loading")

    elif  (options.runType == "full"):
        if len(args) < 3:
            print "Missing some of the required paths."
            sys.exit()
        print "Learning followed by Testing mode."
        learnPath = args[0]
        testPath = args[1]
        outPath = args[2]

        # clean up the output first !
        if os.path.exists(outPath):
            shutil.rmtree(outPath)
        os.mkdir(outPath)

        trainedObjects = train(learnPath, options.threshold)
        cvUtilities = TU.Utils(options.threshold)

        imageDescWriter = IDW.ImageDescriptionWriter()

        for file1 in os.listdir(args[1]):

            # do not use .* files
            if file1.startswith("."):
                continue

            # save output (the name of the object without .bmp / .jpg etc)
            fileName = os.path.basename(file1)
            fileName = os.path.splitext(fileName)[0]
            imgOutPath = os.path.join(outPath, fileName)
            if not os.path.exists(imgOutPath):
                os.mkdir(imgOutPath)

            # with image files do ...
            if not file1.endswith(".imd"):

                # flags are set to 0 = meaning grey scale
                testImage = cv2.imread(os.path.join(args[1], file1), flags=0)
                utils = TU.Utils(options.threshold)
                (kp, desc) = utils.findSURF(testImage, options.threshold)                
                print "Loaded test image : '%s'" % file1

                matcher = FM.FlannMatcher(trainedObjects, options.threshold)
                match = matcher.matchObject(testImage)
                print "Found match for file '%s'" % file1
                
                for obj in match:
                    print "Object Name: ", obj[0].name
                    print "OrientationName: ", obj[0].orientations[obj[1]][0].name
                    with open(os.path.join(imgOutPath, "computed") + ".imd", 'w') as fileStream:
                        imageDescWriter.write(fileStream, obj[0].orientations[obj[1]][0])
                        
                    #below is a badSmell workaround
                    matchedPath = obj[0].orientations[obj[1]][0].name.replace("scripts","renders").replace("runner.","violin.runner.")

                    #show the match
                    matchedImage = cv2.imread(matchedPath, cv2.IMREAD_GRAYSCALE) 
                    vis = utils.draw_match(matchedImage, testImage, obj[4][0], obj[4][1], obj[2], obj[3])
                    cv2.imshow("match!", vis)
                    cv2.waitKey()

            # with .imd files to this
            else :
                src = os.path.join(args[1], file1)
                dst = os.path.join(imgOutPath, "expected.imd")
                print "Coping the file '%s' into '%s'" % (src, dst)
                shutil.copyfile(src, dst)


        print "done full"

