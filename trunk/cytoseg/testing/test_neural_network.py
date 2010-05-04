
import wx
from cytoseg_classify import *

voxelTrainingImageFilePath="data/sbfsem_training/images/small"
voxelTrainingLabelFilePath="data/sbfsem_training/label/small"

app = wx.PySimpleApp()
dataViewer = ClassificationControlsFrame(makeClassifyGUITree())
dataViewer.Show()

original = loadImageStack(voxelTrainingImageFilePath, None)[0:55,0:55,0:9]

dataViewer.addVolumeAndRefreshDataTree_new(
                            rescale(original, 0, 1),
                            ('Volumes', 'OriginalVolume'))

label = loadImageStack(voxelTrainingLabelFilePath, None)[0:55,0:55,0:9]

dataViewer.addVolumeAndRefreshDataTree_new(
                            (label > 0) * 1,
                            ('Volumes', 'LabelVolume'))

learner = NeuralNetworkLearner(dataViewer.getVolume_new(('Volumes', 'OriginalVolume')),
                               dataViewer.getVolume_new(('Volumes', 'LabelVolume')))

updateNeuralNetworkCount = 0

def updateNeuralNetwork():

    global updateNeuralNetworkCount

    learner.update()

    print learner.network.weights

    writeTiffStack(defaultOutputPath,
                   dataViewer.getVolume_new(('Volumes', 'OutputVolume')),
                   baseFileName=("neural_%03d" % updateNeuralNetworkCount))

    updateNeuralNetworkCount += 1

#dataViewer.updateFunctions['updateNeuralNetwork'] = learner.update
dataViewer.updateFunctions['updateNeuralNetwork'] = updateNeuralNetwork
#learner.network.update()

dataViewer.addVolumeAndRefreshDataTree_new(
                            learner.network.getOutput(),
                            ('Volumes', 'OutputVolume'))

app.MainLoop()
