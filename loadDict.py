#CS 2450
#Argument Checking, Directory Walking, and Word List BST

import os
import sys
import random
from BSTree import BSTree

## os.walk() returns a 3-tupple for every directory in a directory tree.
## The first item in each tupple is a string which is the directory's path. (root)
## The second item is a list of strings which are directories in the directory. (dirs in root)
## The third item is a list of strings which are files in the directory. (files in root)

# Receives a directory to be searched. Returns a list of 'bin' file filenames.
def dirWalk(dir):
    binFiles = []

    # If dir is a file, add it to the list and return.
    if os.path.isfile(dir):
        binFiles.append(os.path.abspath(dir))
        return binFiles
    elif os.path.isdir(dir):
        # unpack and loop through every tupple
        for root, dirs, files in os.walk(dir):
            # loop through file names and add only 'bin' files to binFiles[]
            for fname in files:
                if (fname[-3:]).lower() == 'bin':
                    binFiles.append(os.path.join(root, fname))
    else:   #not a file or directory
        fail()

    return binFiles


# checks the command line arguments and populates BST dictionary.
def loadDict():
    # validate command line arguments
    if len(sys.argv) != 2:
        fail()

    # get filenames
    binFiles = dirWalk(sys.argv[1])

    ### populate dictionary
    # get a list of words
    print "Getting words ...",
    dictlist = []
    dictfile = open("dict.txt", 'r')
    for line in dictfile:
        dictlist.append(line)
    dictfile.close()
    print "Done"
    print "Generating BST ...",
    # shuffle the list (don't insert items alphabetically into a BST)
    random.shuffle(dictlist)
    # create BST object, then populate
    dictionary = BSTree()
    for word in dictlist:
        dictionary.Insert(word.strip())
    print "Done"

def fail():
    print "Missing or invalid argument."
    print "Please enter the name of a '.bin' file or directory."
    print "Examples of usage:"
    print "python phonesearch.py nokia.bin"
    print "python phonesearch.py binFiles"
    print "If the path has a space, use quotation marks."
    print 'python phonesearch.py "mystery dump"'
    sys.exit(-1)

loadDict()
