
#from sbfsem import *
import os
import sys
import default_path
from volume3d_util import Box

cytosegDataFolder = r"Z:\cytoseg_data"
default_path.defaultTemporaryFolder = cytosegDataFolder
default_path.cytosegDataFolder = cytosegDataFolder
default_path.contourOutputTemporaryFolder = cytosegDataFolder
default_path.defaultOutputPath = cytosegDataFolder

#for numTrees in (1, 10, 40, 160, 640):
print "sbfsem_batch_contours"

#path = "Z:/blobOutput/"
#path = r"C:\temp"
path = ""

if not(os.path.exists(path)):
    os.mkdir(path)

#zStart = 11
#zStart = 14
#zStop = 15
zStart = 3
#zStart = 6
#zStop = 23
zStop = 7

regionToProcess = Box([None, None, zStart], [None, None, zStop])

from sbfsem import *
sbfsem(r"O:\images\neuropil_test\mitochondria",
       r"O:\images\neuropil_test\mitochondria",
       r"",
       #path, numTrees, 6+1, None, zStart - zStartOffset, zStop + zEndOffset + 1, iteration, taskToPerform)
       path, 25, 6+1, None, None, regionToProcess, 0, 'contours', guiVisible=True,
       configFile='sbfsem_settings1.py')
#command = "%s start_sbfsem.py %s %d %d %d %d" %\
#    (sys.executable, path, numTrees, 6+3, 6+4, iteration, 'contours')
#print command
#os.system(command)

