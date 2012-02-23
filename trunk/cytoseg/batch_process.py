
#from sbfsem import *
import os
import sys
import socket
import re
sys.path.append("..")
import default_path
import getopt
from volume3d_util import Box
from volume3d_util import getImageStackSize
from data_viewer import borderWidthForFeatures
from run_steps import *
import globals
from datetime import datetime


def batchProcessVoxels(segmentationParams, steps, fullRegionToClassify, chunkSize): #todo: make chunkParams a 3D region and a chunk size instea

    f = fullRegionToClassify

    stackSize = getImageStackSize(segmentationParams['originalImageFilePath'])

    if f.cornerA[2] == None:
        f.cornerA[2] = 0;

    if f.cornerB[2] == None:
        f.cornerB[2] = stackSize[2];

    for zOffset in range(f.cornerA[2],
                         f.cornerB[2],
                         chunkSize):
    
    
        print "zOffset:", zOffset
        overlap = 2 * borderWidthForFeatures[2]

        finalZ = zOffset + chunkSize + overlap
        if finalZ > f.cornerB[2]: finalZ = f.cornerB[2]
        
        regionToClassify = Box([f.cornerA[0], f.cornerA[1], zOffset],
                               [f.cornerB[0], f.cornerB[1], finalZ])
    
        segmentationParams['steps'] = steps #'classifyVoxels'
        segmentationParams['regionToClassify'] = regionToClassify

        runSteps(**segmentationParams)



def batchProcessContours(segmentationParams, stepSets, fullRegionToProcess, chunkSize):

    f = fullRegionToProcess

    stackSize = getImageStackSize(segmentationParams['originalImageFilePath'])

    if f.cornerA[2] == None:
        f.cornerA[2] = 0;

    if f.cornerB[2] == None:
        f.cornerB[2] = stackSize[2];

    for zOffset in range(f.cornerA[2],
                         f.cornerB[2],
                         chunkSize):
     
        print "zOffset:", zOffset
        overlap = globals.blobOutputCropZUpper() +\
                  globals.blobOutputCropZLower()
        print "zOffset + chunkSize + overlap:", zOffset + chunkSize + overlap

        initialZ = zOffset
        finalZ = zOffset + chunkSize + overlap

        
        if finalZ > f.cornerB[2]:
            finalZ = f.cornerB[2] # This is neccesary to ensure that the final Z for this chunk doesn't exceed the limit specified.
            initialZ = finalZ - (chunkSize + overlap) # This is neccesary to ensure that the chunk isn't so thin than the level set doesn't work. (Less than 4 won't work.) However, the chunksize needs to be sufficiently big.
            if initialZ < 0:
                raise Exception("chunk size plus overlap is larger than the data in the Z dimension")

        print "initialZ", initialZ
        print "finalZ", finalZ

        contourProcessingRegionToClassify = Box([f.cornerA[0], f.cornerA[1], initialZ],
                                                [f.cornerB[0], f.cornerB[1], finalZ])

        params = dict(segmentationParams)
        params['contourProcessingRegionToClassify'] = contourProcessingRegionToClassify
    
        for stepSet in stepSets:
            params['steps'] = stepSet
            print "starting step", datetime.now()
            runSteps(**params)
            print "finished step", datetime.now()

