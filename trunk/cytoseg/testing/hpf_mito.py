
import sys
sys.path.append("..")

from detector import Detector

param = {}

param['originalImageFilePath'] = "O:/images/HPFcere_vol/HPF_rotated_tif/padding_removed/8bit"
param['voxelTrainingImageFilePath'] = "O:/images/HPFcere_vol/HPF_rotated_tif/three_compartment"
param['voxelTrainingLabelFilePath'] = "O:/images/HPFcere_vol/HPF_rotated_tif/three_compartment/membrane_label_for_three_compartments"
param['blobImageStackOutputFolder'] = "O:/temp/blobOutput"

detector = Detector(param)
detector.dataViewer.mainDoc.dataTree.rootFolderPath = "G:/cytoseg_data/hpf"
detector.contourClassifier.fullManualSegFilePath =\
    "O:/images/HPFcere_vol/HPF_rotated_tif/padding_removed/8bit/segmentation"
#detector.dataIdentifier = "hpf"
#detector.contourTrainer.numberOfLayersToProcess = 14
#detector.contourTrainer.numberOfTrainingLayersToProcess = 7
#detector.contourClassifier.minVoxelLabelValue = 3
detector.run(runAllSteps=0)
