# data location configuration file

import sys
#sys.path.append("..")

from label_identifier import *
from contour_set_detector import ContourSetDetector
from volume3d_util import Box
import default_path


def sbfsem(originalImageFilePath=r"O:\images\ncmirdata1\obayashi\for_TD\3viewdata\080309\wbc_segtrainer_forRG\amira\data_tifs\last55\350x350\crop\8bit\last40\a",
           voxelTrainingImageFilePath=r"O:\images\ncmirdata1\obayashi\for_TD\3viewdata\080309\wbc_segtrainer_forRG\amira\data_tifs\last55\350x350\crop\8bit\last40\b",
           voxelTrainingLabelFilePath=r"O:\images\ncmirdata1\obayashi\for_TD\3viewdata\080309\wbc_segtrainer_forRG\amira\seg_tifs70\50-69\crop",
           blobImageStackOutputFolder="O:/temp/blobOutput_080309",
           numberOfTrees=50,
           numberOfTrainingLayersToProcess=7,
           numberOfLayersToProcess=8,
           classifyStartZ=None,
           classifyEndZ=None,
           voxelClassificationIteration=0,
           steps=False):

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
    detector = ContourSetDetector(param, voxelClassificationIteration,
                                  guiVisible=False)

    #detector.contourClassifier.fullManualSegFilePath = param['voxelTrainingLabelFilePath']
    #detector.contourClassifier.fullManualSegFilePath = "O:/images/ncmirdata1/obayashi/for_TD/3viewdata/080309/wbc_segtrainer_forRG/amira/seg_tifs3/350x350/crop/last/test_seg" + subfolder
    detector.contourClassifier.fullManualSegFilePath = r"O:\images\ncmirdata1\obayashi\for_TD\3viewdata\080309\wbc_segtrainer_forRG\amira\seg_tifs70\30-49\crop"

    detector.dataIdentifier = "sbfsem_080309"
    #detector.dataViewer.mainDoc.dataTree.rootFolderPath = "Z:/cytoseg_data/sbfsem" +\
    #    subfolder
    detector.dataViewer.mainDoc.dataTree.rootFolderPath =\
        default_path.cytosegDataFolder + subfolder
    detector.dataViewer.numberOfTrees = numberOfTrees
    #detector.contourClassifier.numberOfLayersToProcess = 50
    #detector.contourClassifier.numberOfLayersToProcess = 14
    detector.contourClassifier.numberOfLayersToProcess = numberOfLayersToProcess
    detector.contourClassifier.regionToClassify = Box([None, None, classifyStartZ],
                                                      [None, None, classifyEndZ])
    detector.contourClassifier.numberOfTrainingLayersToProcess =\
        numberOfTrainingLayersToProcess
    #detector.contourClassifier.minVoxelLabelValue['mitochondria'] = 3
    #detector.contourClassifier.minVoxelLabelValue['membranes'] = 2
    #detector.contourClassifier.maxVoxelLabelValue['membranes'] = 2
    #detector.contourClassifier.labelIdentifierDict['membranes'] =\
    #    LabelIdentifier(min=100, max=300)
    detector.contourClassifier.labelIdentifierDict['membranes'] =\
        LabelIdentifier(min=2, max=2)
    #detector.contourClassifier.labelIdentifierDict['mitochondria'] =\
    #    LabelIdentifier(min=3, max=250)
    detector.contourClassifier.labelIdentifierDict['mitochondria'] =\
        LabelIdentifier(min=141, max=141)
    #detector.contourClassifier.labelIdentifierDict['blankInnerCell'] =\
    #    LabelIdentifier(min=150, max=150)
    #detector.contourClassifier.labelIdentifierDict['blankInnerCell'] =\
    #    LabelIdentifier(min=0, max=0)
    detector.contourClassifier.labelIdentifierDict['blankInnerCell'] =\
        LabelIdentifier(values=range(3,100+1)+[142])
    ##detector.contourClassifier.labelIdentifierDict['blankInnerCell'] =\
    ##    LabelIdentifier(values=(0,))
    #detector.contourClassifier.labelIdentifierDict['vesicles'] =\
    #    LabelIdentifier(min=255, max=255)
    detector.contourClassifier.labelIdentifierDict['vesicles'] =\
        LabelIdentifier(min=138, max=138)

    # this setting is probably obsolete
    detector.setTarget('membranes')
    #detector.setTarget('membranes_test')

    print "sbfsem.py detector: run", steps
    #detector.dataViewer.mainDoc.dataTree.rootFolderPath = "/home/rsingh/temp"
    #detector.dataViewer.mainDoc.dataTree.rootFolderPath = "C:/temp"
    detector.run(steps)

