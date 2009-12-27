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
    inputImageFilePath = "data/membrane_small_original"
    exampleListFileName = os.path.join(cytosegDataFolder, "exampleList.tab")
    
    voxelTrainingImageNodePath = ('Volumes', 'voxelTrainingImage')
    voxelTrainingLabelNodePath = ('Volumes', 'voxelTrainingLabel')
    inputImageNodePath = ('Volumes', 'inputImage')

    gui.addVolumeAndRefreshDataTree(loadImageStack(voxelTrainingImageFilePath, None),
                                    voxelTrainingImageNodePath[1])

    gui.addVolumeAndRefreshDataTree(loadImageStack(voxelTrainingLabelFilePath, None),
                                    voxelTrainingLabelNodePath[1])
    
    gui.addVolumeAndRefreshDataTree(loadImageStack(inputImageFilePath, None),
                                    inputImageNodePath[1])

    # uses training data
    print "learning features of training data"
    gui.learnFeaturesOfMembraneVoxels(voxelTrainingImageNodePath,
                                      voxelTrainingLabelNodePath,
                                      exampleListFileName)
    
    # uses test data, generates voxel probabilities
    print "classifying voxels"
    gui.classifyVoxels('intermediateDataLabel1',
                       'outputDataLabel1',
                       exampleListFileName,
                       inputImageNodePath)
    
    


app = wx.PySimpleApp()
gui = ClassificationControlsFrame(makeClassifyGUITree())
gui.Show()
mainThread = ProcessingThread(mainFunction)
mainThread.start()
app.MainLoop()
