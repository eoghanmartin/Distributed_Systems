import sys, pdb

class Files():
    
    FILES = []

    def newFileCreated(self, newFileName, fileDetailsFile):
        with open(fileDetailsFile, "a") as fileDetails:
            fileDetails.write("\n" + newFileName)
        fileDetails.close()

    def setupFilesList(self, fileDetailsFile):
        global FILES
        FILES = []
        with open(fileDetailsFile) as f:
            file_details = f.readlines()
        f.close()
        for l in file_details:
            nextItem = l.replace("\n", "")
            FILES.append(nextItem)
        print (str(len(FILES)))

    def checkForFile(self, fileNameString):
        global FILES
        #pdb.set_trace()
        if fileNameString in FILES:
            return True
        else:
            return False
