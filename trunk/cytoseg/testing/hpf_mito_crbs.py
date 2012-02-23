import sys
sys.path.append("..")

from detector import Detector

param = {}

# each volume is a stack of 8 bit tiff images


# full input volume
param['originalImageFilePath']="/home/rgiuly/images/HPFcere_vol/HPF_rotated_tif/padding_removed/8bit"

# training data image volume
param['voxelTrainingImageFilePath']="/home/rgiuly/images/HPFcere_vol/HPF_rotated_tif/three_compartment"

# training data label, 0 for nonmitochondria pixels, 1 for mitochondria pixels
# this should have the exact same dimensions as param['voxelTrainingImageFilePath'] 
param['voxelTrainingLabelFilePath']="/home/rgiuly/images/HPFcere_vol/HPF_rotated_tif/three_compartment/membrane_label_for_three_compartments"

# output volume
param['blobImageStackOutputFolder']="/home/rgiuly/temp/blobOutput"

Detector(param)
