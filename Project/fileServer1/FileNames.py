import sys, pdb
import os

class Files():
    
    FILES = []

    def setupFilesList(self):
        global FILES
        FILES = []
        for file in os.listdir("./files"):
            FILES.append(file)
        #print (FILES)

    def checkForFile(self, fileNameString):
        global FILES
        #pdb.set_trace()
        if fileNameString + '.txt' in FILES:
            return True
        else:
            return False
