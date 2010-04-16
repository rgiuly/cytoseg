
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

#for numTrees in (1, 10, 40, 160, 640):
print "sbfsem_batch"
for numTrees in (25,):

    for iteration in range(1, 2):

        path = "Z:/blobOutput_numberOfTrees/" + str(numTrees)

        if not(os.path.exists(path)):
            os.mkdir(path)

        from sbfsem import *
        sbfsem(path, numTrees, 6+1, 6+2, iteration, 'contours')
        #command = "%s start_sbfsem.py %s %d %d %d %d" %\
        #    (sys.executable, path, numTrees, 6+3, 6+4, iteration, 'contours')
        #print command
        #os.system(command)

