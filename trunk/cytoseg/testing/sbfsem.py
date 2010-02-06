# data location configuration file

import sys
sys.path.append("..")

from label_identifier import *

from contour_set_detector import ContourSetDetector


def sbfsem(blobImageStackOutputFolder="O:/temp/blobOutput_080309",
           numberOfTrees=50,
           numberOfTrainingLayersToProcess=7,
           numberOfLayersToProcess=8):

    param = {}

    # each volume is a stack of 8 bit tiff images


    #subfolder = ""
    subfolder = "/small_crop"
    #subfolder = "/tiny_crop"

    # full input volume
    #param['originalImageFilePath'] = "data/sbfsem_080309/data_tifs"
    param['originalImageFilePath'] = "O:/images/ncmirdata1/obayashi/for_TD/3viewdata/080309/wbc_segtrainer_forRG/amira/data_tifs/last/8bit/350x350/crop" + subfolder

    # training data image volume
    #param['voxelTrainingImageFilePath'] = "data/sbfsem_080309/data_tifs"
    param['voxelTrainingImageFilePath'] = "O:/images/ncmirdata1/obayashi/for_TD/3viewdata/080309/wbc_segtrainer_forRG/amira/data_tifs/last/8bit/350x350/crop" + subfolder

    # training data labels
    # this should have the exact same dimensions as param['voxelTrainingImageFilePath'] 
    #param['voxelTrainingLabelFilePath'] = "O:/images/ncmirdata1/obayashi/for_TD/3viewdata/080309/wbc_segtrainer_forRG/amira/seg_tifs/350x350/vesicles_and_membranes" + subfolder
    param['voxelTrainingLabelFilePath'] = "O:/images/ncmirdata1/obayashi/for_TD/3viewdata/080309/wbc_segtrainer_forRG/amira/seg_tifs/350x350/crop" + subfolder

    # output volume
    param['blobImageStackOutputFolder'] = blobImageStackOutputFolder

    #detector = Detector(param)
    detector = ContourSetDetector(param)
    detector.dataIdentifier = "sbfsem_080309"
    detector.dataViewer.mainDoc.dataTree.rootFolderPath = "G:/cytoseg_data/sbfsem" +\
        subfolder
    detector.dataViewer.numberOfTrees = numberOfTrees
    #detector.contourClassifier.numberOfLayersToProcess = 50
    #detector.contourClassifier.numberOfLayersToProcess = 14
    detector.contourClassifier.numberOfLayersToProcess = numberOfLayersToProcess
    detector.contourClassifier.numberOfTrainingLayersToProcess =\
        numberOfTrainingLayersToProcess
    #detector.contourClassifier.minVoxelLabelValue['mitochondria'] = 3
    #detector.contourClassifier.minVoxelLabelValue['membranes'] = 2
    #detector.contourClassifier.maxVoxelLabelValue['membranes'] = 2
    detector.contourClassifier.labelIdentifierDict['membranes'] =\
        LabelIdentifier(min=2, max=2)
    #detector.contourClassifier.labelIdentifierDict['mitochondria'] =\
    #    LabelIdentifier(min=3, max=250)
    #detector.contourClassifier.labelIdentifierDict['blankInnerCell'] =\
    #    LabelIdentifier(min=150, max=150)
    detector.contourClassifier.labelIdentifierDict['blankInnerCell'] =\
        LabelIdentifier(min=0, max=0)
    detector.contourClassifier.labelIdentifierDict['vesicles'] =\
        LabelIdentifier(min=255, max=255)
    detector.setTarget('membranes')
    #detector.setTarget('membranes_test')
    detector.run(runAllSteps=0)
