#This software is Copyright © 2012 The Regents of the University of California. All Rights Reserved.
#Permission to use, copy, modify, and distribute this software and its documentation for educational, research and non-profit purposes for non-profit institutions, without fee, and without a written agreement is hereby granted, provided that the above copyright notice, this paragraph and the following three paragraphs appear in all copies.
#Permission to make commercial use of this software may be obtained by contacting:
#Technology Transfer Office
#9500 Gilman Drive, Mail Code 0910
#University of California
#La Jolla, CA 92093-0910
#(858) 534-5815
#invent@ucsd.edu
#This software program and documentation are copyrighted by The Regents of the University of California. The software program and documentation are supplied "as is", without any accompanying services from The Regents. The Regents does not warrant that the operation of the program will be uninterrupted or error-free. The end-user understands that the program was developed for research purposes and is advised not to rely exclusively on the program for any reason.
#IN NO EVENT SHALL THE UNIVERSITY OF CALIFORNIA BE LIABLE TO
#ANY PARTY FOR DIRECT, INDIRECT, SPECIAL, INCIDENTAL, OR
#CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING
#OUT OF THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION,
#EVEN IF THE UNIVERSITY OF CALIFORNIA HAS BEEN ADVISED OF
#THE POSSIBILITY OF SUCH DAMAGE. THE UNIVERSITY OF
#CALIFORNIA SPECIFICALLY DISCLAIMS ANY WARRANTIES,
#INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
#MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#THE SOFTWARE PROVIDED HEREUNDER IS ON AN "AS IS" BASIS, AND THE UNIVERSITY OF CALIFORNIA HAS NO OBLIGATIONS TO
#PROVIDE MAINTENANCE, SUPPORT, UPDATES, ENHANCEMENTS, OR
#MODIFICATIONS.

# Reads command line arguments and executes process


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


# Variable initializations

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
    """Convert comma separated list string on command line to list of numbers."""

    coordinates = re.split(",", arg)
    for i in range(len(coordinates)):
        if coordinates[i] == "*":
            coordinates[i] = None;
        else:
            coordinates[i] = int(coordinates[i])
    return coordinates



def usage():
    """Print usage information."""
    print "For usage, see http://code.google.com/p/cytoseg/wiki/Usage"






def voxelStep(stepName):
    """
    Run a voxel processing step on a volume.
    Each chunk of the volume is loaded separately.
    """

    print "voxelSingleStep", stepName
    batchProcessVoxels(segmentationParams,
                       stepName,
                       voxelFullRegionToClassify,
                       voxelChunkSize)


def contourSingleStep_old(stepName):
    """Deprecated"""

    print "contourSingleStep", stepName

    segmentationParams['guiVisible'] = False

    batchProcessContours(segmentationParams,
                         (stepName,),
                         contourProcessingRegion,
                         contourChunkSize)


def contourSingleStep(stepName):
    """
    Execute a substep (given by stepName) in the contour processing step of the segmentation process.
    segmentationParams variable has detailed information about the process.
    """

    print "contourSingleStep", stepName

    segmentationParams['guiVisible'] = False
    segmentationParams['contourProcessingRegionToClassify'] = contourProcessingRegion
    segmentationParams['steps'] = stepName

    runSteps(**segmentationParams)


def contourStepSet():
    """
    Execute all substeps of the contour process phase of the segmentation process.
    segmentationParams variable has detailed information about the process.
    """

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
    """Run step that classifies the training voxels."""

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







# Process command line arguments
#try:
opts, args = getopt.gnu_getopt(sys.argv, "", ["trainingImage=", "trainingSeg=", "voxelTrainingLowerBound=", "voxelTrainingUpperBound=", "voxelProcessingLowerBound=", "voxelProcessingUpperBound=", "contourTrainingLowerBound=", "contourTrainingUpperBound=", "contourProcessingLowerBound=", "contourProcessingUpperBound=", "accuracyCalcLowerBound=", "accuracyCalcUpperBound=", "labelConfigFile=", "voxelWeights=", "contourListWeights=", "contourListThreshold=", "step1", "step2"])
print "opts, args", opts, args
#except getopt.GetoptError as e:
#    print "Error processing command line arguments"
#    print e
#    usage()
#    sys.exit(2)
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
                  precomputedTrainingProbabilityMapFilePath=os.path.join(cytosegDataFolder, "voxelOutput", "training", "mitochondria", "resized"),
                  precomputedInputProbabilityMapFilePath=os.path.join(cytosegDataFolder, "voxelOutput", "mitochondria", "resized"),
                  blobImageStackOutputFolder=os.path.join(cytosegDataFolder, "voxelOutput"),
                  numberOfTrees=25,
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


#voxelChunkSize=1;

if not(runStep1) and not(runStep2):
    """Ensure that the user specified steps to run."""
    raise Exception("No steps specified. You may use parameters such as --step1 and --step2 to specify what steps to run.")


# Run step 1 if the user specified it (voxel processing)
if runStep1:
    print "segmentationParams 1", segmentationParams
    print "contourProcessingRegion 1", contourProcessingRegion
    voxelStep('classifyVoxels')
    #classifyTrainingVoxelsStep()


# Run step 2 if the user specified it (contour and level set processing)
if runStep2:
    print "segmentationParams 2", segmentationParams
    print "contourProcessingRegion 2", contourProcessingRegion
    classifyTrainingVoxelsStep()
    # todo: create another function similar to voxelStep but for functions that are to be run just once rather than as a piece of a batch process
    print "segmentationParams 3", segmentationParams
    print "contourProcessingRegion 3", contourProcessingRegion
    contourSingleStep('findTrainingContours')
    print "segmentationParams 4", segmentationParams
    print "contourProcessingRegion 4", contourProcessingRegion
    contourSingleStep('classifyTrainingContours')
    #contourChunkSize = 4
    print "segmentationParams 5", segmentationParams
    print "contourProcessingRegion 5", contourProcessingRegion
    contourStepSet()
    #contourSingleStep('accuracy')

