
#from sbfsem import *
import os
import sys
sys.path.append("..")
import math
import default_path

from command_reader import CommandReader

enableMPI = 1

if enableMPI:
    # MPI code
    from mpi4py import MPI
    
    comm = MPI.COMM_WORLD
    mpiRank = comm.Get_rank()
    mpiCommSize = comm.Get_size()
else:
    mpiRank = 0
    mpiCommSize = 10

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

logging.basicConfig(level=logging.DEBUG,
                    filename=os.path.join(cytosegDataFolder, 'log.txt'))

#for numTrees in (1, 10, 40, 160, 640):
print "sbfsem_batch"
for numTrees in (25,):

    for iteration in range(0, 1):

        path = param['blobImageStackOutputFolder'] + str(numTrees)
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

            sbfsem(param['originalImageFilePath'],
       	           param['voxelTrainingImageFilePath'],
       	           param['voxelTrainingLabelFilePath'],
       	           #path, numTrees, 6+1, None, zStart - zStartOffset, zStop + zEndOffset + 1, iteration, taskToPerform)
                   path, numTrees, 6+1, None, zStart, zStop, iteration, taskToPerform)
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

