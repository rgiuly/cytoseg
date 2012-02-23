
#from sbfsem import *
import os
import sys
import socket
import re
sys.path.append("..")
import default_path
import getopt
from volume3d_util import Box
from data_viewer import borderWidthForFeatures

#cytosegDataFolder = r"Z:\cytoseg_data"
#cytosegDataFolder = r"O:\Z_drive\cytoseg_data"

originalImageFilePath="/jane-temp/rgiuly/guttman_data/8bit"
voxelTrainingImageFilePath="/jane-temp/rgiuly/guttman_data/8bit"
voxelTrainingLabelFilePath="/jane-temp/rgiuly/guttman_seg/8bit/grayscale"

configFile="settings2.py"

if socket.gethostname() == 'cytoseg.crbs.ucsd.edu':
    baseFolder = "/home/rgiuly"
elif socket.gethostname() == 'cluster0.crbs.ucsd.edu':
    baseFolder = "/export2/rgiuly"
elif socket.gethostname() == 'jane.crbs.ucsd.edu':
    baseFolder = "/jane-temp/rgiuly"
else:
    baseFolder = "O:"

#trainingRegion = Box([200, 200, 200], [400, 400, 207])
#regionToClassify = Box([100, 400, 203], [620, 700, 210])
#trainingRegion = Box([0, 0, 200], [700, 700, 220])
#regionToClassify = Box([200, 200, 150], [700, 700, 158])
#trainingRegion = Box([0, 0, 200], [700, 700, 215]) #paper
trainingRegion = Box([4961, 1966, 110], [5464, 2195, 220])
#trainingRegion = Box([0, 0, 220], [400, 400, 227])
#regionToClassify = Box([0, 0, 148], [700, 700, 160])
#regionToProcess = Box([100, 200, 203], [220, 700, 210])
#regionToProcess = Box([200, 200, 203], [250, 250, 210])

regionToClassifyX1 = 0
regionToClassifyY1 = 0
regionToClassifyZ1 = 0
regionToClassifyX2 = 2000
regionToClassifyY2 = 2000
regionToClassifyZ2 = 270


def usage():
    print "usage: sbfsem_batch_voxels_test input output --trainingData directory --trainingSeg directory"

try:
    opts, args = getopt.gnu_getopt(sys.argv, "", ["trainingData=", "trainingSeg=", "voxelTrainingLowerBound=", "voxelTrainingUpperBound=", "voxelProcessingLowerBound=", "voxelProcessingUpperBound=", "contourTrainingLowerBound=", "contourTrainingUpperBound=", "contourProcessingLowerBound=", "contourProcessingUpperBound=", "labelConfigFile="])
    print "opts, args", opts, args
except getopt.GetoptError:
    print "Error processing command line arguments"
    usage()
    sys.exit(2)
if len(args) >= 2: originalImageFilePath = args[1]
if len(args) >= 3: baseFolder = args[2]
for opt, arg in opts:
    if opt == "--trainingData":
        voxelTrainingImageFilePath = arg

    if opt == "--trainingSeg":
        voxelTrainingLabelFilePath = arg

    if opt == "--voxelTrainingLowerBound":
        coordinates = re.split(",", arg)
        for index in range(0, 3):
            trainingRegion.cornerA[index] = int(coordinates[index])

    if opt == "--voxelTrainingUpperBound":
        coordinates = re.split(",", arg)
        for index in range(0, 3):
            trainingRegion.cornerB[index] = int(coordinates[index])

    if opt == "--voxelProcessingLowerBound":
        coordinates = re.split(",", arg)
        regionToClassifyX1 = int(coordinates[0])
        regionToClassifyY1 = int(coordinates[1])
        regionToClassifyZ1 = int(coordinates[2])

    if opt == "--voxelProcessingUpperBound":
        coordinates = re.split(",", arg)
        regionToClassifyX2 = int(coordinates[0])
        regionToClassifyY2 = int(coordinates[1])
        regionToClassifyZ2 = int(coordinates[2])

    if opt == "--labelConfigFile":
        configFile = arg


print "Parameters:"
print "originalImageFilePath", originalImageFilePath
print "baseFolder", baseFolder
print "voxelTrainingImageFilePath", voxelTrainingImageFilePath
print "voxelTrainingLabelFilePath", voxelTrainingLabelFilePath

print "regionToClassify1", regionToClassifyX1, regionToClassifyY1, regionToClassifyZ1
print "regionToClassify2", regionToClassifyX2, regionToClassifyY2, regionToClassifyZ2

print "trainingRegion", trainingRegion

print

cytosegDataFolder = os.path.join(baseFolder, "cytoseg_data")
default_path.defaultTemporaryFolder = cytosegDataFolder
default_path.cytosegDataFolder = cytosegDataFolder
default_path.contourOutputTemporaryFolder = cytosegDataFolder
default_path.defaultOutputPath = cytosegDataFolder

#for numTrees in (1, 10, 40, 160, 640):
print "sbfsem_batch_contours"

#path = "Z:/blobOutput/"
#path = r"C:\temp"
path = os.path.join(cytosegDataFolder, "voxelOutput")

if not(os.path.exists(path)):
    os.mkdir(path)



from sbfsem import *

#chunkSize = 15
chunkSize = 5
guiVisible = False


#for zOffset in range(200, 270, chunkSize):
for zOffset in range(regionToClassifyZ1, regionToClassifyZ2, chunkSize):
#for zOffset in range(215, 230, chunkSize):
#for zOffset in range(200, 202, chunkSize):

    print "zOffset:", zOffset
    overlap = 2 * borderWidthForFeatures[2]
    #regionToClassify = Box([0, 0, zOffset], #IEEE paper
    #                       [700, 700, zOffset + chunkSize + overlap]) #IEEE paper
    regionToClassify = Box([regionToClassifyX1, regionToClassifyY1, zOffset],
                           [regionToClassifyX2, regionToClassifyY2, zOffset + chunkSize + overlap])

    sbfsem(
           #originalImageFilePath=os.path.join(baseFolder,"images/neuropil/data"),
           #voxelTrainingImageFilePath=os.path.join(baseFolder,"images/neuropil/data"),
           #voxelTrainingLabelFilePath=os.path.join(baseFolder,"images/neuropil/seg"),
           originalImageFilePath=originalImageFilePath,
           voxelTrainingImageFilePath=voxelTrainingImageFilePath,
           voxelTrainingLabelFilePath=voxelTrainingLabelFilePath,
           #path, numTrees, 6+1, None, zStart - zStartOffset, zStop + zEndOffset + 1, iteration, taskToPerform)
           blobImageStackOutputFolder=path,
           numberOfTrees=25,
           #numberOfTrainingLayersToProcess=6+1,
           numberOfTrainingLayersToProcess=None,
           trainingRegion=trainingRegion,
           numberOfLayersToProcess=None,
           regionToClassify=regionToClassify,
           voxelClassificationIteration=0,
           steps='classifyVoxels',
           guiVisible=guiVisible,
           configFile=configFile
           #configFile='sbfsem_settings1.py' used for IEEE paper
           )
#command = "%s start_sbfsem.py %s %d %d %d %d" %\
#    (sys.executable, path, numTrees, 6+3, 6+4, iteration, 'contours')
#print command
#os.system(command)

for i in range(5):
    print chr(7)

