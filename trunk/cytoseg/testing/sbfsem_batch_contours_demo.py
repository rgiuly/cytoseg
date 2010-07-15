
#from sbfsem import *
import os
import sys
sys.path.append("..")
import default_path
from volume3d_util import Box

cytosegDataFolder = r"O:\cytoseg_data_demo"
default_path.defaultTemporaryFolder = cytosegDataFolder
default_path.cytosegDataFolder = cytosegDataFolder
default_path.contourOutputTemporaryFolder = cytosegDataFolder
default_path.defaultOutputPath = cytosegDataFolder

#for numTrees in (1, 10, 40, 160, 640):
print "sbfsem_batch_contours"

#stepSet = 'contours'
stepSet = 'classifyContours'

#path = "Z:/blobOutput/"
#path = r"C:\temp"
path = ""

#if not(os.path.exists(path)):
#    os.mkdir(path)

zStart = 203
zStop = 207
#zStop = 204

regionToProcess = Box([None, None, zStart], [None, None, zStop])

from sbfsem import *
sbfsem(originalImageFilePath=r"O:\images\neuropil\data",
       voxelTrainingImageFilePath="",
       voxelTrainingLabelFilePath=r"O:\images\neuropil\seg",
       precomputedProbabilityMapFilePath=r"O:\images\neuropil\mitochondria",
       #path, numTrees, 6+1, None, zStart - zStartOffset, zStop + zEndOffset + 1, iteration, taskToPerform)
       blobImageStackOutputFolder=path,
       numberOfTrees=25,
       numberOfTrainingLayersToProcess=6+1,
       trainingRegion=regionToProcess,
       numberOfLayersToProcess=None,
       regionToClassify=regionToProcess,
       voxelClassificationIteration=0,
       steps=stepSet,
       guiVisible=True,
       configFile='sbfsem_settings1.py')
#command = "%s start_sbfsem.py %s %d %d %d %d" %\
#    (sys.executable, path, numTrees, 6+3, 6+4, iteration, 'contours')
#print command
#os.system(command)

