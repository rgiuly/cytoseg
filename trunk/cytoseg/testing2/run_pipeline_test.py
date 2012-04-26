
import os
import sys
import socket
import re
sys.path.append("..")
import default_path
import getopt
from volume3d_util import Box
from data_viewer import borderWidthForFeatures
from batch_process import *
import logging
import copy

originalImageFilePath = None

#trainingRegion = Box([4961, 1966, 110], [5464, 2195, 220])
trainingRegion = Box()
contourProcessingRegion = Box()
contourTrainingRegion = Box()
accuracyCalcRegion = Box()

regionToClassifyX1 = None
regionToClassifyY1 = None
regionToClassifyZ1 = None
regionToClassifyX2 = None
regionToClassifyY2 = None
regionToClassifyZ2 = None

runStep1 = False
runStep2 = False

voxelWeightDict = {'foreground':1, 'background':1}
contourListWeightDict = {True:1, False:1}
contourListThreshold = 0.5

#accuracyCalcRegion = Box([None, None, 216], [None, None, 230]) # BMC Bioinformatics paper for cerebellum
#accuracyCalcRegion = Box([None, None, 61], [None, None, 76])


def interpretCoordinateString(coordinates):
    coordinates = re.split(",", arg)
    for i in range(len(coordinates)):
        if coordinates[i] == "*":
            coordinates[i] = None;
        else:
            coordinates[i] = int(coordinates[i])
    return coordinates

def usage():
    print "usage: sbfsem_batch_voxels_test input output --trainingImage directory --trainingSeg directory"

try:
    opts, args = getopt.gnu_getopt(sys.argv, "", ["trainingImage=", "trainingSeg=", "voxelTrainingLowerBound=", "voxelTrainingUpperBound=", "voxelProcessingLowerBound=", "voxelProcessingUpperBound=", "contourTrainingLowerBound=", "contourTrainingUpperBound=", "contourProcessingLowerBound=", "contourProcessingUpperBound=", "accuracyCalcLowerBound=", "accuracyCalcUpperBound=", "labelConfigFile=", "voxelWeights=", "contourListWeights=", "contourListThreshold=", "step1", "step2"])
    print "opts, args", opts, args
except getopt.GetoptError as e:
    print "Error processing command line arguments"
    print e
    usage()
    sys.exit(2)
if len(args) >= 2: originalImageFilePath = args[1]
if len(args) >= 3: cytosegDataFolder = args[2]
for opt, arg in opts:
    if opt == "--trainingImage":
        voxelTrainingImageFilePath = arg

    if opt == "--trainingSeg":
        voxelTrainingLabelFilePath = arg

    if opt == "--voxelTrainingLowerBound":
        coordinates = interpretCoordinateString(arg)
        for index in range(0, 3):
            trainingRegion.cornerA[index] = coordinates[index]

    if opt == "--voxelTrainingUpperBound":
        coordinates = interpretCoordinateString(arg)
        for index in range(0, 3):
            trainingRegion.cornerB[index] = coordinates[index]

    if opt == "--voxelProcessingLowerBound":
        coordinates = interpretCoordinateString(arg)
        regionToClassifyX1 = coordinates[0]
        regionToClassifyY1 = coordinates[1]
        regionToClassifyZ1 = coordinates[2]

    if opt == "--voxelProcessingUpperBound":
        coordinates = interpretCoordinateString(arg)
        regionToClassifyX2 = coordinates[0]
        regionToClassifyY2 = coordinates[1]
        regionToClassifyZ2 = coordinates[2]

    if opt == "--contourTrainingLowerBound":
        coordinates = interpretCoordinateString(arg)
        for index in range(0, 3):
            contourTrainingRegion.cornerA[index] = coordinates[index]

    if opt == "--contourTrainingUpperBound":
        coordinates = interpretCoordinateString(arg)
        for index in range(0, 3):
            contourTrainingRegion.cornerB[index] = coordinates[index]

    if opt == "--contourProcessingLowerBound":
        coordinates = interpretCoordinateString(arg)
        for index in range(0, 3):
            contourProcessingRegion.cornerA[index] = coordinates[index]

    if opt == "--contourProcessingUpperBound":
        coordinates = interpretCoordinateString(arg)
        for index in range(0, 3):
            contourProcessingRegion.cornerB[index] = coordinates[index]

    if opt == "--accuracyCalcLowerBound":
        coordinates = interpretCoordinateString(arg)
        for index in range(0, 3):
            accuracyCalcRegion.cornerA[index] = coordinates[index]

    if opt == "--accuracyCalcUpperBound":
        coordinates = interpretCoordinateString(arg)
        for index in range(0, 3):
            accuracyCalcRegion.cornerB[index] = coordinates[index]

    if opt == "--labelConfigFile":
        configFile = arg

    if opt == "--voxelWeights":
        numbers = re.split(",", arg)
        voxelWeightDict['foreground'] = float(numbers[0])
        voxelWeightDict['background'] = float(numbers[1])

    if opt == "--contourListWeights":
        numbers = re.split(",", arg)
        contourListWeightDict[True] = int(numbers[0])
        contourListWeightDict[False] = int(numbers[1])

    if opt == "--contourListThreshold":
        contourListThreshold = float(arg)

    if opt == "--step1":
        runStep1 = True

    if opt == "--step2":
        runStep2 = True

if originalImageFilePath == None:
    print "Error: No input data specified"
    sys.exit()

print "Parameters:"

print "runStep1", runStep1
print "runStep2", runStep2

print "originalImageFilePath", originalImageFilePath
print "cytosegDataFolder", cytosegDataFolder
print "voxelTrainingImageFilePath", voxelTrainingImageFilePath
print "voxelTrainingLabelFilePath", voxelTrainingLabelFilePath

print "regionToClassify1", regionToClassifyX1, regionToClassifyY1, regionToClassifyZ1
print "regionToClassify2", regionToClassifyX2, regionToClassifyY2, regionToClassifyZ2

print "trainingRegion", trainingRegion

print "contourTrainingRegion", contourTrainingRegion
print "contourProcessingRegion", contourProcessingRegion

print "accuracyCalcRegion", accuracyCalcRegion

print "voxelWeightDict", voxelWeightDict
print "contourListWeightDict", contourListWeightDict
print "contourListThreshold", contourListThreshold


print





#if socket.gethostname() == 'cytoseg.crbs.ucsd.edu':
#    baseFolder = "/home/rgiuly/"
#elif socket.gethostname() == 'cluster0.crbs.ucsd.edu':
#    #todo: missing ending slash caused error, it shouldn't really
#    baseFolder = "/export2/rgiuly/"
#elif socket.gethostname() == 'jane.crbs.ucsd.edu':
#    baseFolder = "/tmp/output080309/"
#else:
#    baseFolder = "O:/"

default_path.defaultTemporaryFolder = cytosegDataFolder
default_path.cytosegDataFolder = cytosegDataFolder
default_path.contourOutputTemporaryFolder = cytosegDataFolder
default_path.defaultOutputPath = cytosegDataFolder
default_path.defaultPath = cytosegDataFolder

logFile = os.path.join(default_path.cytosegDataFolder, 'log.txt')
print "logFile", logFile
logging.basicConfig(level=logging.DEBUG,
                    filename=logFile)


voxelOutputPath = os.path.join(cytosegDataFolder, "voxelOutput")
if not(os.path.exists(voxelOutputPath)):
    os.mkdir(voxelOutputPath)

segmentationParams =\
                  dict(originalImageFilePath=originalImageFilePath,
                  voxelTrainingImageFilePath=voxelTrainingImageFilePath,
                  voxelTrainingLabelFilePath=voxelTrainingLabelFilePath,
                  voxelWeightDict=voxelWeightDict,
                  #precomputedProbabilityMapFilePath=baseFolder+"images/neuropil/mitochondria",
                  #precomputedProbabilityMapFilePath=baseFolder+"cytoseg_data/voxelOutput_training_200_to_215/mitochondria/resized", #IEEE paper
                  precomputedTrainingProbabilityMapFilePath=os.path.join(cytosegDataFolder, "voxelOutput", "training", "mitochondria", "resized"),
                  precomputedInputProbabilityMapFilePath=os.path.join(cytosegDataFolder, "voxelOutput", "mitochondria", "resized"),
                  #path, numTrees, 6+1, None, zStart - zStartOffset, zStop + zEndOffset + 1, iteration, taskToPerform)
                  blobImageStackOutputFolder=os.path.join(cytosegDataFolder, "voxelOutput"),
                  numberOfTrees=25,
                  #numberOfTrainingLayersToProcess=6+1,
                  numberOfTrainingLayersToProcess=None,
                  trainingRegion=trainingRegion,
                  numberOfLayersToProcess=None,
                  regionToClassify=None,
                  voxelClassificationIteration=0,
                  contourProcessingTrainingRegion=contourTrainingRegion,
                  contourProcessingRegionToClassify=contourProcessingRegion,
                  contourListWeightDict=contourListWeightDict,
                  contourListThreshold=contourListThreshold,
                  accuracyCalcRegion=accuracyCalcRegion,
                  steps=None,
                  guiVisible=False,
                  configFile=configFile)

voxelFullRegionToClassify = Box([regionToClassifyX1, regionToClassifyY1, regionToClassifyZ1],
                                [regionToClassifyX2, regionToClassifyY2, regionToClassifyZ2])
voxelChunkSize = 5
contourChunkSize = 6 #8


voxelChunkingParams = dict(zStart=230, zStop=240, chunkSize=5)
contourChunkingParams = dict(zStart=230, zStop=238, chunkSize=5)


def voxelStep(stepName):

    print "voxelSingleStep", stepName
    batchProcessVoxels(segmentationParams,
                       stepName,
                       voxelFullRegionToClassify,
                       voxelChunkSize)


def contourSingleStep_old(stepName):

    print "contourSingleStep", stepName

    segmentationParams['guiVisible'] = False

    #stepSets = ['findTrainingContours']
    #stepSets = ['classifyTrainingContours'] # shows accuracy measure
    #stepSets = ['findInputContours']
    #stepSets = ['classifyInputContours']
    #stepSets = ['writeAllInputContoursToImageStack']
    #stepSets = ['inputContourListProbabilityFilter']
    #stepSets = ['fill3DBlobs']
    #stepSets = ['voxelAccuracy'] #old
    #stepSets = ['accuracy']

    batchProcessContours(segmentationParams,
                         (stepName,),
                         contourProcessingRegion,
                         contourChunkSize)


def contourSingleStep(stepName):

    print "contourSingleStep", stepName

    segmentationParams['guiVisible'] = False
    segmentationParams['contourProcessingRegionToClassify'] = contourProcessingRegion
    segmentationParams['steps'] = stepName

    runSteps(**segmentationParams)


def contourStepSet():

    segmentationParams['guiVisible'] = False

    stepSets = ['findInputContours',
                'classifyInputContours',
                'writeAllInputContoursToImageStack',
                'inputContourListProbabilityFilter',
                'fill3DBlobs']

    print "contourStepSet", stepSets

    batchProcessContours(segmentationParams,
                         stepSets,
                         contourProcessingRegion,
                         contourChunkSize)


def classifyTrainingVoxelsStep():

    # use the training images as input
    segmentationParamsCopy = copy.deepcopy(segmentationParams)
    segmentationParamsCopy['originalImageFilePath'] = segmentationParamsCopy['voxelTrainingImageFilePath'] 

    # use the contour training region as the region to be classified
    fullRegion = segmentationParamsCopy['contourProcessingTrainingRegion']

    # classify voxels and send output to appropriate folder
    stepName = 'classifyVoxelsAndUseTrainingOutputFolder'
    batchProcessVoxels(segmentationParamsCopy,
                       stepName,
                       fullRegion,
                       voxelChunkSize)


#voxelChunkSize=1;

if not(runStep1) and not(runStep2):
    raise Exception("No steps specified. You may use parameters such as --step1 and --step2 to specify what steps to run.")

if runStep1:
    voxelStep('classifyVoxels')
    classifyTrainingVoxelsStep()

#voxelStep('classifyTrainingVoxels')

if runStep2:
    #voxelChunkSize=8; voxelStep('randonLikeFeaturesProcess') # todo: you probably want another function sort of like voxelStep but for function that are to be run just once rather than as a piece of a batch process
    contourSingleStep('findTrainingContours')
    contourSingleStep('classifyTrainingContours')
    #contourChunkSize = 4
    contourStepSet()
    #contourSingleStep('accuracy')

