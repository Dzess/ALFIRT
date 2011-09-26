'''
Created on 05-05-2011

@author: Ankhazam & Dzess

'''

from optparse import OptionParser
import sys
import os
import shutil
from algorithms import NewFlannMatchingAlgorithm

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


if __name__ == '__main__':
    print "Matcher Learning and Testing Application"

    # set up all the paths
    pathSetUp()

    # proceed with imports
    try:
        from algorithms.FlannMatchingAlgorithm import FlannMatchingAlgorithm
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

        # clean up the output first ! (non algorithm dependent element)
        if os.path.exists(outPath):
            shutil.rmtree(outPath)
        os.mkdir(outPath)

        # running the algorithm
        algorithm = NewFlannMatchingAlgorithm.NewFlannMatchingAlgorithm()

        algorithm.learn(learnPath)
        algorithm.test(testPath, outPath)

        print "done full"

