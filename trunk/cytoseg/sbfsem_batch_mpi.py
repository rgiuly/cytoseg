
#from sbfsem import *
import os
import sys
#sys.path.append("..")
import math
import logging
import default_path
import warnings

from command_reader import CommandReader

try:
    # MPI code
    from mpi4py import MPI
    
    comm = MPI.COMM_WORLD
    mpiRank = comm.Get_rank()
    mpiCommSize = comm.Get_size()
except ImportError:
    warnings.warn("mpi4py module is not installed")
    mpiRank = 0
    mpiCommSize = 1

print "DISPLAY", os.getenv("DISPLAY")

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

#if 0:
#
#    originalImageFilePath = "/home/rsingh/data/machine_learning_tutorial/b"
#    voxelTrainingImageFilePath = "/home/rsingh/data/machine_learning_tutorial/a"
#    voxelTrainingLabelFilePath = "/home/rsingh/data/machine_learning_tutorial/a_membranes"
#
#
#    defaultTemporaryFolder = "/home/rsingh/temp"
#    cytosegDataFolder = "/home/rsingh/temp"
#
#    blobImageStackOutputFolder = "/home/rsingh/temp/"
#
#
#if 1:
#
#    originalImageFilePath = "C:/temp/machine_learning_tutorial/b"
#    voxelTrainingImageFilePath = "C:/temp/machine_learning_tutorial/a"
#    voxelTrainingLabelFilePath = "C:/temp/machine_learning_tutorial/a_membranes"
#
#
#    defaultTemporaryFolder = "C:/temp"
#    cytosegDataFolder = "C:/temp"
#
#    blobImageStackOutputFolder = "C:/temp"

commandReader = CommandReader()
param = commandReader.param
cytosegDataFolder = os.path.join(param['cytosegDataFolder'], "process%03d" % mpiRank)
print "cytosegDataFolder", cytosegDataFolder
if not(os.path.exists(cytosegDataFolder)):
    os.mkdir(cytosegDataFolder)
default_path.defaultTemporaryFolder = cytosegDataFolder
default_path.cytosegDataFolder = cytosegDataFolder
default_path.contourOutputTemporaryFolder = cytosegDataFolder
default_path.defaultOutputPath = cytosegDataFolder

logFile = os.path.join(cytosegDataFolder, 'log.txt')
print "logFile", logFile
logging.basicConfig(level=logging.DEBUG,
                    filename=logFile)

#for numTrees in (1, 10, 40, 160, 640):
print "sbfsem_batch"
for numTrees in (25,):

    for iteration in range(0, 1):

        path = param['blobImageStackOutputFolder']# + str(numTrees)
        numberOfLayersToClassify = 6 + 1

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
	    
#            zSlices = 9
#            zStartOffset = 3
#            zEndOffset = 3
#            zMax = zSlices - zEndOffset
#            zBlock = math.ceil((zMax - zStartOffset) / mpiCommSize)
#            print "zBlock", zBlock
#	    
#            zStart = zStartOffset + zBlock * mpiRank 
#            zStop = zStart + zBlock - 1
#            if(zStop > (zMax - 1)):
#                zStop = zMax - 1
            zStart = mpiRank
            zStop = mpiRank + 6 + 1

            print "Process # ", mpiRank, " -> ", zStart, zStop

            #trainingRegion = Box((0, 0, 0), (170, 170, 7))
            #regionToClassify = Box((0, 0, zStart), (170, 170, zStop))
            #trainingRegion = Box((200, 200, 200), (400, 400, 207))
            trainingRegion = Box((None, None, 200), (None, None, 270))
            #trainingRegion = Box((None, None, 200), (None, None, 207))
            #regionToClassify = Box([100, 400, 203 + mpiRank],
            #                       [620, 700, 210 + mpiRank])

        #for sliceNum in range (0, 1):
        for sliceNum in range (0, 250):
	
            print "(sliceNum + 1)", (sliceNum + 1)
            print "(mpiRank + 1)", (mpiRank + 1)

            if( (sliceNum + 1) % (mpiRank + 1) != 0):
             continue	

            if 1:

                #regionToClassify = Box([100, 400, sliceNum],
                #                       [620, 700, sliceNum + 7])
                regionToClassify = Box([None, None, sliceNum],
                                       [None, None, sliceNum + 7])

                sbfsem(originalImageFilePath=param['originalImageFilePath'],
                        voxelTrainingImageFilePath=param['voxelTrainingImageFilePath'],
                        voxelTrainingLabelFilePath=param['voxelTrainingLabelFilePath'],
                        #path, numTrees, 6+1, None, zStart - zStartOffset, zStop + zEndOffset + 1, iteration, taskToPerform)
                   	    blobImageStackOutputFolder=path,
                        numberOfTrees=numTrees,
                        numberOfTrainingLayersToProcess=6+5,
                        trainingRegion=trainingRegion,
                   	    numberOfLayersToProcess=None,
                        regionToClassify=regionToClassify,
                        voxelClassificationIteration=iteration,
                   	    steps=taskToPerform,
                        guiVisible=False,
                        configFile=param['configFile'])
            #print "zStart - zStartOffset", zStart - zStartOffset
	    #print "zStop + zEndOffset", zStop + zEndOffset
            #sbfsem(param['originalImageFilePath'],
            #       param['voxelTrainingImageFilePath'],
            #       param['voxelTrainingLabelFilePath'],
            #       path, numTrees, 6+1, None, 0, 7, iteration, taskToPerform)
            #sbfsem(param['originalImageFilePath'],
            #       param['voxelTrainingImageFilePath'],
            #       param['voxelTrainingLabelFilePath'],
            #       path, numTrees, 6+1, None, 1, 8, iteration, taskToPerform)

