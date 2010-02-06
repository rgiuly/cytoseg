
from sbfsem import *
import os

#for trainingLayers in (1, 2, 4, 8):
#
#    path = "G:/blobOutput_with_focus/" + str(trainingLayers)
#
#    if not(os.path.exists(path)):
#        os.mkdir(path)
#
#    sbfsem(path, 6 + trainingLayers, 20)

#for numTrees in (1, 10, 40, 160, 640):
for numTrees in (25,):

    path = "G:/blobOutput_numberOfTrees/" + str(numTrees)

    if not(os.path.exists(path)):
        os.mkdir(path)

    sbfsem(path, numTrees, 6+1, 6+2)

