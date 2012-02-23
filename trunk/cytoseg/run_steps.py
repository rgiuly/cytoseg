# This file configures the values of labels corresponding to each object.

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
             #classifyStartZ=None,
             #classifyEndZ=None,
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

    print "configFile", os.path.join(os.getcwd(), 'settings2.py')
    config_file_module = imp.load_source('config_file_module', configFile)

    param = {}

    # each volume is a stack of 8 bit tiff images


    subfolder = ""
    #subfolder = "/small_crop"
    #subfolder = "/tiny_crop"

    # full input volume
    #param['originalImageFilePath'] = "data/sbfsem_080309/data_tifs"
    #param['originalImageFilePath'] = "O:/images/ncmirdata1/obayashi/for_TD/3viewdata/080309/wbc_segtrainer_forRG/amira/data_tifs/last/8bit/350x350/crop" + subfolder
    #param['originalImageFilePath'] = "O:/images/ncmirdata1/obayashi/for_TD/3viewdata/080309/wbc_segtrainer_forRG/amira/data_tifs/last/8bit/350x350/crop/43-51" + subfolder
    #param['originalImageFilePath'] = "O:/images/ncmirdata1/obayashi/for_TD/3viewdata/080309/wbc_segtrainer_forRG/amira/data_tifs/last55/350x350/crop/8bit/last" + subfolder
    #param['originalImageFilePath'] = "O:/images/ncmirdata1/obayashi/for_TD/3viewdata/080309/wbc_segtrainer_forRG/amira/data_tifs/last55/350x350/crop/8bit/last/test" + subfolder
    param['originalImageFilePath'] = originalImageFilePath

    # training data image volume
    #param['voxelTrainingImageFilePath'] = "data/sbfsem_080309/data_tifs"
    #param['voxelTrainingImageFilePath'] = "O:/images/ncmirdata1/obayashi/for_TD/3viewdata/080309/wbc_segtrainer_forRG/amira/data_tifs/last/8bit/350x350/crop" + subfolder
    #param['voxelTrainingImageFilePath'] = "O:/images/ncmirdata1/obayashi/for_TD/3viewdata/080309/wbc_segtrainer_forRG/amira/data_tifs/last/8bit/350x350/crop/43-51" + subfolder
    #param['voxelTrainingImageFilePath'] = "O:/images/ncmirdata1/obayashi/for_TD/3viewdata/080309/wbc_segtrainer_forRG/amira/data_tifs/last55/350x350/crop/8bit/last" + subfolder
    #param['voxelTrainingImageFilePath'] = "O:/images/ncmirdata1/obayashi/for_TD/3viewdata/080309/wbc_segtrainer_forRG/amira/data_tifs/last55/350x350/crop/8bit/last/training" + subfolder
    param['voxelTrainingImageFilePath'] = voxelTrainingImageFilePath

    # training data labels
    # this should have the exact same dimensions as param['voxelTrainingImageFilePath'] 
    #param['voxelTrainingLabelFilePath'] = "O:/images/ncmirdata1/obayashi/for_TD/3viewdata/080309/wbc_segtrainer_forRG/amira/seg_tifs/350x350/vesicles_and_membranes" + subfolder
    #param['voxelTrainingLabelFilePath'] = "O:/images/ncmirdata1/obayashi/for_TD/3viewdata/080309/wbc_segtrainer_forRG/amira/seg_tifs/350x350/crop" + subfolder
    #param['voxelTrainingLabelFilePath'] = "O:/images/ncmirdata1/obayashi/for_TD/3viewdata/080309/wbc_segtrainer_forRG/amira/seg_tifs2/350x350/crop/43-51" + subfolder
    #param['voxelTrainingLabelFilePath'] = "O:/images/ncmirdata1/obayashi/for_TD/3viewdata/080309/wbc_segtrainer_forRG/amira/seg_tifs3/350x350/crop/last" + subfolder
    #param['voxelTrainingLabelFilePath'] = "O:/images/ncmirdata1/obayashi/for_TD/3viewdata/080309/wbc_segtrainer_forRG/amira/seg_tifs3/350x350/crop/last/training_seg" + subfolder
    param['voxelTrainingLabelFilePath'] = voxelTrainingLabelFilePath

    # output volume
    param['blobImageStackOutputFolder'] = blobImageStackOutputFolder

    #detector = Detector(param)
    detector = SegmentationManager(param, voxelClassificationIteration,
                                   guiVisible=guiVisible)

    #detector.componentDetector.fullManualSegFilePath = param['voxelTrainingLabelFilePath']
    #detector.componentDetector.fullManualSegFilePath = "O:/images/ncmirdata1/obayashi/for_TD/3viewdata/080309/wbc_segtrainer_forRG/amira/seg_tifs3/350x350/crop/last/test_seg" + subfolder
    detector.componentDetector.fullManualSegFilePath = r"O:\images\ncmirdata1\obayashi\for_TD\3viewdata\080309\wbc_segtrainer_forRG\amira\seg_tifs70\30-49\crop"

    detector.dataIdentifier = "sbfsem_080309"
    #detector.dataViewer.mainDoc.dataTree.rootFolderPath = "Z:/cytoseg_data/sbfsem" +\
    #    subfolder
    detector.dataViewer.mainDoc.dataTree.rootFolderPath =\
        default_path.cytosegDataFolder + subfolder
    detector.dataViewer.numberOfTrees = numberOfTrees
    #detector.componentDetector.numberOfLayersToProcess = 50
    #detector.componentDetector.numberOfLayersToProcess = 14
    detector.componentDetector.numberOfLayersToProcess = numberOfLayersToProcess
    detector.componentDetector.regionToClassify = regionToClassify
    #detector.contourTrainer.numberOfLayersToProcess = numberOfLayersToProcess
    #detector.contourTrainer.regionToClassify = regionToClassify
    #detector.componentDetector.regionToClassify = Box([None, None, classifyStartZ],
    #                                                  [None, None, classifyEndZ])
    detector.componentDetector.numberOfTrainingLayersToProcess =\
        numberOfTrainingLayersToProcess
    #detector.contourTrainer.numberOfTrainingLayersToProcess =\
    #    numberOfTrainingLayersToProcess

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
    #detector.contourTrainer.precomputedProbabilityMapFilePath =\
    #    precomputedProbabilityMapFilePath

    #detector.setTarget('membranes_test')

    detector.componentDetector.accuracyCalcRegion = accuracyCalcRegion

    detector.componentDetector.voxelWeightDict = voxelWeightDict
    detector.componentDetector.contourListWeightDict = contourListWeightDict
    detector.componentDetector.contourListProbabilityThreshold = contourListThreshold

    print "sbfsem.py detector: run", steps
    #detector.dataViewer.mainDoc.dataTree.rootFolderPath = "/home/rsingh/temp"
    #detector.dataViewer.mainDoc.dataTree.rootFolderPath = "C:/temp"
    detector.run(steps)

