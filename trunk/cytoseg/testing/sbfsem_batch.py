
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

#for numTrees in (1, 10, 40, 160, 640):
print "sbfsem_batch"
for numTrees in (25,):

    for iteration in range(0, 5):

        path = "G:/blobOutput_numberOfTrees/" + str(numTrees)

        if not(os.path.exists(path)):
            os.mkdir(path)

        # true or false
        multipleProcesses = 1

        if multipleProcesses:

            #command = "%s start_sbfsem.py %s %d %d %d %d %s" %\
            #    (sys.executable, path, numTrees, 6+4, 6+1, iteration, taskToPerform)
            command = "%s start_sbfsem.py %s %d %d %d %d %s" %\
                (sys.executable, path, numTrees, 6+4, 6+20, iteration, taskToPerform)
            print command
            os.system(command)

        else:

            from sbfsem import *
            #sbfsem(path, numTrees, 6+1, 6+2, iteration, taskToPerform)
            sbfsem(path, numTrees, 6+4, 6+20, iteration, taskToPerform)

