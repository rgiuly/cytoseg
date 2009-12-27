import sys
sys.path.append("..")

from detector import Detector

param = {}

# each volume is a stack of 8 bit tiff images


# full input volume
param['originalImageFilePath']="data/sbfsem_080309/data_tifs"

# training data image volume
param['voxelTrainingImageFilePath']="o:/images/HPFcere_vol/HPF_rotated_tif/three_compartment"

# training data label, 0 for nonmitochondria pixels, 1 for mitochondria pixels
# this should have the exact same dimensions as param['voxelTrainingImageFilePath'] 
param['voxelTrainingLabelFilePath']="o:/images/HPFcere_vol/HPF_rotated_tif/three_compartment/membrane_label_for_three_compartments"

# output volume
param['blobImageStackOutputFolder']="o:/temp/blobOutput_080309"

Detector(param)
