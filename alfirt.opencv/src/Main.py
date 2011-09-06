'''
Created on 05-05-2011

@author: Ankhazam
'''

from optparse import OptionParser
import sys
import os

def train(learningPath):
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
    for (root,dirs,files) in os.walk(learningPath):
        print "root: ",root
        for dir1 in dirs:
            print "dir: ", dir1
        for file1 in files:
            print "file: ", file1

if __name__ == '__main__':
    print "Matcher Learning and Testing Application"
    
    parser = OptionParser(usage="usage: %prog [options] [learning_files_path/dbase_file_path] [test_files_path] [results_path]")
    parser.add_option("-r", "--runType", action="store", dest="runType", type="str",
        help="Run selection learn|test|full. \"learn\" requires 1st path, \"test\"  2nd and 3rd, \"full\" all three of them.",
        default="test")
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
        train(learnPath)
        raise NotImplementedError("To be added")
    
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
        
        raise NotImplementedError("To be added")
