
#from sbfsem import *
import os
import sys
import default_path

cytosegDataFolder = r"Z:\cytoseg_data"
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

zStart = 11
#zStart = 14
zStop = 15

from sbfsem import *
sbfsem(r"O:\images\neuropil_test\mitochondria",
       r"O:\images\neuropil_test\mitochondria",
       r"Z:\cytoseg_data",
       #path, numTrees, 6+1, None, zStart - zStartOffset, zStop + zEndOffset + 1, iteration, taskToPerform)
       path, 25, 6+1, None, zStart, zStop, 0, 'contours', guiVisible=True)
#command = "%s start_sbfsem.py %s %d %d %d %d" %\
#    (sys.executable, path, numTrees, 6+3, 6+4, iteration, 'contours')
#print command
#os.system(command)

