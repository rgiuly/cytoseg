
#from sbfsem import *
import os
import sys

#for trainingLayers in (1, 2, 4, 8):
#
#    path = "G:/blobOutput_with_focus/" + str(trainingLayers)
#
#    if not(os.path.exists(path)):
#        os.mkdir(path)
#
#    sbfsem(path, 6 + trainingLayers, 20)

#taskToPerform = 'accuracy'
taskToPerform = 'classifyVoxels'

#subfolder = r"\30x30"
subfolder = ""
originalImageFilePath = r"O:\images\ncmirdata1\obayashi\for_TD\3viewdata\080309\wbc_segtrainer_forRG\amira\data_tifs\last55\350x350\crop\8bit\last40\a" + subfolder
voxelTrainingImageFilePath = r"O:\images\ncmirdata1\obayashi\for_TD\3viewdata\080309\wbc_segtrainer_forRG\amira\data_tifs\last55\350x350\crop\8bit\last40\b" + subfolder
voxelTrainingLabelFilePath = r"O:\images\ncmirdata1\obayashi\for_TD\3viewdata\080309\wbc_segtrainer_forRG\amira\seg_tifs70\50-69\crop" + subfolder

#for numTrees in (1, 10, 40, 160, 640):
print "sbfsem_batch"
for numTrees in (25,):

    for iteration in range(0, 1):

        path = "Z:/blobOutput_numberOfTrees/" + str(numTrees)
        numberOfLayersToClassify = 6 + 3

        if not(os.path.exists(path)):
            os.mkdir(path)

        # true or false
        startNewProcesses = 0

        if startNewProcesses:

            #command = "%s start_sbfsem.py %s %d %d %d %d %s" %\
            #    (sys.executable, path, numTrees, 6+4, 6+1, iteration, taskToPerform)
            command = "%s start_sbfsem.py %s %d %d %d %d %s" %\
                (sys.executable, path, numTrees, 6+1, 6+1, iteration, taskToPerform)
            print command
            os.system(command)

        else:

            from sbfsem import *
            #sbfsem(path, numTrees, 6+1, 6+2, iteration, taskToPerform)
            sbfsem(originalImageFilePath,
                   voxelTrainingImageFilePath,
                   voxelTrainingLabelFilePath,
                   path, numTrees, 6+1, None, 5, 5+numberOfLayersToClassify, iteration, taskToPerform)

