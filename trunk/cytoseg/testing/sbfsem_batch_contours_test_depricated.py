# Instructions:
# run with singleStep = 1 and stepSets = ['findTrainingContours']
# run with singleStep = 1 and stepSets = ['classifyTrainingContours'] # shows accuracy measure
# run with singleStep = 0


#from sbfsem import *
import os
import sys
sys.path.append("..")
import default_path
import socket
from datetime import datetime

from volume3d_util import Box
#import component_detector # this messes up a path
import globals

print "sbfsem_batch_contours"

singleStep = 0

if singleStep:

    #guiVisible = True
    guiVisible = False

    #stepSets = ['findTrainingContours']
    stepSets = ['classifyTrainingContours'] # shows accuracy measure
    #stepSets = ['findInputContours']
    #stepSets = ['classifyInputContours']
    #stepSets = ['writeAllInputContoursToImageStack']
    #stepSets = ['inputContourListProbabilityFilter']
    #stepSets = ['fill3DBlobs']
    #stepSets = ['voxelAccuracy'] #old
    #stepSets = ['accuracy']


else:

    guiVisible = False
    #guiVisible = True

    stepSets = ['findInputContours',
                'classifyInputContours',
                'writeAllInputContoursToImageStack',
                'inputContourListProbabilityFilter',
                'fill3DBlobs']


if socket.gethostname() == 'cytoseg.crbs.ucsd.edu':
    baseFolder = "/home/rgiuly/"
elif socket.gethostname() == 'cluster0.crbs.ucsd.edu':
    #todo: missing ending slash caused error, it shouldn't really
    baseFolder = "/export2/rgiuly/"
elif socket.gethostname() == 'jane.crbs.ucsd.edu':
    baseFolder = "/tmp/output080309/"
else:
    baseFolder = "O:/"

cytosegDataFolder = os.path.join(baseFolder, "cytoseg_data")
default_path.defaultTemporaryFolder = cytosegDataFolder
default_path.cytosegDataFolder = cytosegDataFolder
default_path.contourOutputTemporaryFolder = cytosegDataFolder
default_path.defaultOutputPath = cytosegDataFolder

#for numTrees in (1, 10, 40, 160, 640):

blobImageStackOutputFolder = os.path.join(cytosegDataFolder, "blobOutput")
#trainingRegion = Box([None, None, 230], [None, None, 232])
#regionToClassify = Box([None, None, 200], [None, None, 202])
trainingRegion = Box([None, None, None], [None, None, None])
regionToClassify = Box([None, None, None], [None, None, None])

#contourProcessingTrainingRegion = Box([None, None, 200], [None, None, 205])
#contourProcessingTrainingRegion = Box([None, None, 200], [None, None, 207])
#contourProcessingTrainingRegion = Box([None, None, 200], [None, None, 210])
#contourProcessingTrainingRegion = Box([None, None, 200], [None, None, 215]) #IEEE settings
contourProcessingTrainingRegion = Box([0, 0, 230], [600, 600, 238])

#accuracyCalcRegion = Box([None, None, 241], [None, None, 249])
accuracyCalcRegion = Box([None, None, 216], [None, None, 230])
#accuracyCalcRegion = Box([None, None, 216], [None, None, 221])
# small z separation causes error
#accuracyCalcRegion = Box([None, None, 190], [None, None, 204])



segmentationParameters =\
                  dict(originalImageFilePath=baseFolder+"images/neuropil/data",
                  voxelTrainingImageFilePath=baseFolder+"images/neuropil/data",
                  voxelTrainingLabelFilePath=baseFolder+"images/neuropil/seg",
                  #precomputedProbabilityMapFilePath=baseFolder+"images/neuropil/mitochondria",
                  #precomputedProbabilityMapFilePath=baseFolder+"cytoseg_data/voxelOutput_training_200_to_215/mitochondria/resized", #IEEE paper
                  precomputedProbabilityMapFilePath=baseFolder+"cytoseg_data/voxelOutput/mitochondria/resized",
                  #path, numTrees, 6+1, None, zStart - zStartOffset, zStop + zEndOffset + 1, iteration, taskToPerform)
                  blobImageStackOutputFolder=blobImageStackOutputFolder,
                  numberOfTrees=25,
                  numberOfTrainingLayersToProcess=6+1,
                  trainingRegion=trainingRegion,
                  numberOfLayersToProcess=None,
                  regionToClassify=regionToClassify,
                  voxelClassificationIteration=0,
                  contourProcessingTrainingRegion=contourProcessingTrainingRegion,
                  contourProcessingRegionToClassify=None,
                  accuracyCalcRegion=accuracyCalcRegion,
                  steps=None,
                  guiVisible=guiVisible,
                  configFile='settings1.py')





if not(os.path.exists(blobImageStackOutputFolder)):
    os.mkdir(blobImageStackOutputFolder)

#zStart = 203
#zStop = 207
#zStop = 204


#contourProcessingRegionToClassify = Box([None, None, 100], [None, None, 104])
#contourProcessingRegionToClassify = Box([None, None, 100], [None, None, 132])
#contourProcessingRegionToClassify = Box([None, None, 80], [None, None, 84])
#contourProcessingRegionToClassify = Box([None, None, 0], [None, None, 40])
#contourProcessingRegionToClassify = Box([None, None, 55], [None, None, 75])


from run_steps import *

chunkSize = 5
#chunkSize = 11
#chunkSize = 15 #IEEE

#rangeList = range(221, 270, chunkSize)
#rangeList = range(221, 232, chunkSize)
#rangeList = range(214, 225, chunkSize)
#rangeList = range(0, 270, chunkSize)
rangeList = range(230, 238, chunkSize)

print "rangeList:", rangeList
print "stepSets:", stepSets



for zOffset in rangeList:

    print "zOffset:", zOffset
    overlap = globals.blobOutputCropZUpper() +\
              globals.blobOutputCropZLower()
    print "zOffset + chunkSize + overlap", zOffset + chunkSize + overlap
    contourProcessingRegionToClassify = Box([0, 0, zOffset],
                                            [600, 600, zOffset + chunkSize + overlap])

    segmentationParameters['contourProcessingRegionToClassify'] = contourProcessingRegionToClassify

#if 1:

    for stepSet in stepSets:
        segmentationParameters['steps'] = stepSet
        print "starting step", datetime.now()
        runSteps(**segmentationParameters)
        print "finished step", datetime.now()
#command = "%s start_sbfsem.py %s %d %d %d %d" %\
#    (sys.executable, path, numTrees, 6+3, 6+4, iteration, 'contours')
#print command
#os.system(command)

