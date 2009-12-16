
from detector import Detector

param = {}

param['originalImageFilePath']="/home/rgiuly/images/HPFcere_vol/HPF_rotated_tif/padding_removed/8bit"
param['voxelTrainingImageFilePath']="/home/rgiuly/images/HPFcere_vol/HPF_rotated_tif/three_compartment"
param['voxelTrainingLabelFilePath']="/home/rgiuly/images/HPFcere_vol/HPF_rotated_tif/three_compartment/membrane_label_for_three_compartments"
param['blobImageStackOutputFolder']="/home/rgiuly/temp/blobOutput"

Detector(param)
