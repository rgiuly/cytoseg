
#from sbfsem import *
import os
import sys
sys.path.append("..")
import default_path
from volume3d_util import Box

#cytosegDataFolder = r"Z:\cytoseg_data"
cytosegDataFolder = r"O:\Z_drive\cytoseg_data"
default_path.defaultTemporaryFolder = cytosegDataFolder
default_path.cytosegDataFolder = cytosegDataFolder
default_path.contourOutputTemporaryFolder = cytosegDataFolder
default_path.defaultOutputPath = cytosegDataFolder

#for numTrees in (1, 10, 40, 160, 640):
print "sbfsem_batch_contours"

path = "Z:/blobOutput/"
#path = r"C:\temp"

if not(os.path.exists(path)):
    os.mkdir(path)


trainingRegion = Box((200, 200, 200), (400, 400, 207))
regionToProcess = Box([100, 400, 203], [620, 700, 210])
#regionToProcess = Box([100, 200, 203], [220, 700, 210])
#regionToProcess = Box([200, 200, 203], [250, 250, 210])

from sbfsem import *
sbfsem(r"O:\images\neuropil\data",
       r"O:\images\neuropil\data",
       r"O:\images\neuropil\seg",
       #path, numTrees, 6+1, None, zStart - zStartOffset, zStop + zEndOffset + 1, iteration, taskToPerform)
       path, 25, 6+1, trainingRegion,
       None, regionToProcess, 0, 'classifyVoxels', guiVisible=True,
       configFile='sbfsem_settings1.py')
#command = "%s start_sbfsem.py %s %d %d %d %d" %\
#    (sys.executable, path, numTrees, 6+3, 6+4, iteration, 'contours')
#print command
#os.system(command)

