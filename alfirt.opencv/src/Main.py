'''
Created on 05-05-2011

@author: Ankhazam
'''

from optparse import OptionParser
import sys


 


if __name__ == '__main__':
    print "Matcher Learning and Testing Application"
    
    parser = OptionParser(usage="usage: %prog [options] [learning_files_path] [test_files_path] [results_path]")
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
    elif (options.runType == "test"):
        if len(args) < 2:
            print "Missing some of the required paths (need testing_images_directory and output_directory)."
            sys.exit()
        print "Testing mode"
        testPath = args[0]
        outPath = args[1]
    elif  (options.runType == "full"):
        if len(args) < 3:
            print "Missing some of the required paths."
            sys.exit()
        print "Learning followed by Testing mode."
        learnPath = args[0]
        testPath = args[1]
        outPath = args[2]
    
    
    

