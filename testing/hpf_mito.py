
from detector import Detector

param = {}

param['originalImageFilePath']="O:/images/HPFcere_vol/HPF_rotated_tif/padding_removed/8bit"
param['voxelTrainingImageFilePath']="O:/images/HPFcere_vol/HPF_rotated_tif/three_compartment"
param['voxelTrainingLabelFilePath']="O:/images/HPFcere_vol/HPF_rotated_tif/three_compartment/membrane_label_for_three_compartments"
param['blobImageStackOutputFolder']="O:/temp/blobOutput"

Detector(param)
