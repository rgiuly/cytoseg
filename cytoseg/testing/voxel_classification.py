import sys
sys.path.append("..")

from cytoseg_classify import *
from default_path import *

class ProcessingThread(threading.Thread):

#todo: make a class like this that you can pass an arbitary function to and have it run the function in the thread
    
    def __init__(self, functionToRun):
        threading.Thread.__init__(self)
        self.functionToRun = functionToRun
    
    def run(self):
        self.functionToRun()


def mainFunction():
    
    voxelTrainingImageFilePath = "data/membrane_training/image"
    voxelTrainingLabelFilePath = "data/membrane_training/label"
    inputImageFilePath = "data/membrane"
    exampleListFileName = os.path.join(cytosegDataFolder, "exampleList.tab")
    
    # uses training data
    print "learning features of training data"
    gui.learnFeaturesOfMembraneVoxels(voxelTrainingImageFilePath, voxelTrainingLabelFilePath, exampleListFileName)
    
    # uses test data, generates voxel probabilities
    print "classifying voxels"
    gui.classifyVoxels('intermediateDataLabel1', 'outputDataLabel1', exampleListFileName, inputImageFilePath)
    
    numpyArray = loadImageStack("data/3D-blob-data", None)
    
    gui.addVolumeAndRefreshDataTree(numpyArray, "numpyArray")
    


app = wx.PySimpleApp()
gui = ClassificationControlsFrame(makeClassifyGUITree())
gui.Show()
mainThread = ProcessingThread(mainFunction)
mainThread.start()
app.MainLoop()
