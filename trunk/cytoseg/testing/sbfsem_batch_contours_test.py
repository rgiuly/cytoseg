
#from sbfsem import *
import os
import sys
sys.path.append("..")
import default_path
from volume3d_util import Box

#baseFolder = "O:/"
baseFolder = "/home/rgiuly/"

cytosegDataFolder = baseFolder + "cytoseg_data"
default_path.defaultTemporaryFolder = cytosegDataFolder
default_path.cytosegDataFolder = cytosegDataFolder
default_path.contourOutputTemporaryFolder = cytosegDataFolder
default_path.defaultOutputPath = cytosegDataFolder

#for numTrees in (1, 10, 40, 160, 640):
print "sbfsem_batch_contours"

#stepSet = 'findTrainingContours'
#stepSet = 'classifyTrainingContours'
#stepSet = 'findInputContours'
stepSet = 'classifyInputContours'
#stepSet = 'findInputContoursTest'

#path = "Z:/blobOutput/"
#path = r"C:\temp"
path = ""

#if not(os.path.exists(path)):
#    os.mkdir(path)

#zStart = 203
#zStop = 207
#zStop = 204

trainingRegion = Box([None, None, 230], [None, None, 232])
regionToClassify = Box([None, None, 200], [None, None, 202])
contourProcessingTrainingRegion = Box([None, None, 240], [None, None, 244])
contourProcessingRegionToClassify = Box([None, None, 100], [None, None, 104])

from sbfsem import *
sbfsem(originalImageFilePath=baseFolder+"images/neuropil/data",
       voxelTrainingImageFilePath="",
       voxelTrainingLabelFilePath=baseFolder+"images/neuropil/seg",
       precomputedProbabilityMapFilePath=baseFolder+"images/neuropil/mitochondria",
       #path, numTrees, 6+1, None, zStart - zStartOffset, zStop + zEndOffset + 1, iteration, taskToPerform)
       blobImageStackOutputFolder=path,
       numberOfTrees=25,
       numberOfTrainingLayersToProcess=6+1,
       trainingRegion=trainingRegion,
       numberOfLayersToProcess=None,
       regionToClassify=regionToClassify,
       voxelClassificationIteration=0,
       contourProcessingTrainingRegion=contourProcessingTrainingRegion,
       contourProcessingRegionToClassify=contourProcessingRegionToClassify,
       steps=stepSet,
       guiVisible=True,
       configFile='sbfsem_settings1.py')
#command = "%s start_sbfsem.py %s %d %d %d %d" %\
#    (sys.executable, path, numTrees, 6+3, 6+4, iteration, 'contours')
#print command
#os.system(command)

