# runSteps function to create SegmentationManager object and execute task

import sys
import os
#sys.path.append("..")

#from label_identifier import *

from segmentation_manager import SegmentationManager

from volume3d_util import Box
import default_path
import imp
print "runSteps"


def runSteps(originalImageFilePath=None,
             voxelTrainingImageFilePath=None,
             voxelTrainingLabelFilePath=None,
             voxelWeightDict=None,
             precomputedTrainingProbabilityMapFilePath=None,
             precomputedInputProbabilityMapFilePath=None,
             blobImageStackOutputFolder=None,
             numberOfTrees=50,
             numberOfTrainingLayersToProcess=7,
             trainingRegion=None,
             numberOfLayersToProcess=8,
             regionToClassify=None,
             voxelClassificationIteration=0,
             contourProcessingTrainingRegion=None,
             contourProcessingRegionToClassify=None,
             contourListWeightDict=None,
             contourListThreshold=None,
             accuracyCalcRegion=None,
             steps=None,
             guiVisible=False,
             configFile=os.path.join(os.getcwd(), 'settings2.py')):
    """
    Run segmentation steps
    Parameters:
    originalImageFilePath: file path to input image data
    voxelTrainingImageFilePath: file path to training image
    voxelTrainingLabelFilePath: file path to training labels that correspond to training image
    voxelWeightDict: indicates the factors to balance number of training examples for voxels
    precomputedTrainingProbabilityMapFilePath: path to image stack that's the probability map for voxels
    precomputedInputProbabilityMapFilePath: path to image stack that's the training probability map for voxels
    blobImageStackOutputFolder: folder where output blobs are written
    numberOfTrees: number of trees to used with random forest
    numberOfTrainingLayersToProcess: optional limit on number of training layers to process. (None for all)
    trainingRegion: region of training data to use (None for the whole volume)
    numberOfLayersToProcess: optional limit on number of layers to process. (None for all)
    regionToClassify: region of the input image data to classify. (None for all)
    voxelClassificationIteration: current voxel classification iteration when using series architecture
    contourProcessingTrainingRegion: region of training data to use for contour training
    contourProcessingRegionToClassify: region of the input data on which to do contour-based process
    contourListWeightDict: weighting to balance examples for training with contour lists
    contourListThreshold: threshold used to decide if a contour list is salient
    accuracyCalcRegion: region in which to calculate accuracy of segmentation,
    steps: segmentation steps to execute,
    guiVisible: True to make the GUI visible, False otherwise
    configFile: full path to config file that indicates how label values map to objects
    """

    print "configFile", os.path.join(os.getcwd(), 'settings2.py')
    config_file_module = imp.load_source('config_file_module', configFile)

    param = {}

    # each volume is a stack of 8 bit tiff images


    subfolder = ""
    #subfolder = "/small_crop"
    #subfolder = "/tiny_crop"

    # full input volume
    param['originalImageFilePath'] = originalImageFilePath

    # training data image volume
    param['voxelTrainingImageFilePath'] = voxelTrainingImageFilePath

    # training data labels
    # this should have the exact same dimensions as param['voxelTrainingImageFilePath'] 
    param['voxelTrainingLabelFilePath'] = voxelTrainingLabelFilePath

    # output volume
    param['blobImageStackOutputFolder'] = blobImageStackOutputFolder

    #detector = Detector(param)
    detector = SegmentationManager(param, voxelClassificationIteration,
                                   guiVisible=guiVisible)

    detector.componentDetector.fullManualSegFilePath = r"O:\images\ncmirdata1\obayashi\for_TD\3viewdata\080309\wbc_segtrainer_forRG\amira\seg_tifs70\30-49\crop"

    detector.dataIdentifier = "sbfsem_080309"
    detector.dataViewer.mainDoc.dataTree.rootFolderPath =\
        default_path.cytosegDataFolder + subfolder
    detector.dataViewer.numberOfTrees = numberOfTrees
    detector.componentDetector.numberOfLayersToProcess = numberOfLayersToProcess
    detector.componentDetector.regionToClassify = regionToClassify
    detector.componentDetector.numberOfTrainingLayersToProcess =\
        numberOfTrainingLayersToProcess

    config_file_module.mapNumbersToComponents(detector)
    detector.componentDetector.trainingRegion = trainingRegion
    #detector.contourTrainer.trainingRegion = trainingRegion

    #detector.contourTrainer.contourTrainingRegion = trainingRegion
    detector.componentDetector.contourTrainingRegion = trainingRegion

    detector.componentDetector.contourProcessingTrainingRegion =\
        contourProcessingTrainingRegion
    detector.componentDetector.contourProcessingRegionToClassify =\
        contourProcessingRegionToClassify

    detector.componentDetector.precomputedTrainingProbabilityMapFilePath =\
        precomputedTrainingProbabilityMapFilePath
    detector.componentDetector.precomputedInputProbabilityMapFilePath =\
        precomputedInputProbabilityMapFilePath

    detector.componentDetector.accuracyCalcRegion = accuracyCalcRegion

    detector.componentDetector.voxelWeightDict = voxelWeightDict
    detector.componentDetector.contourListWeightDict = contourListWeightDict
    detector.componentDetector.contourListProbabilityThreshold = contourListThreshold

    print "sbfsem.py detector: run", steps

    detector.run(steps)

