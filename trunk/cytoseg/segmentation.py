# Utility functions: Dijkstra's algorithm and flood fill


from numpy import *
import heapq
from collections import defaultdict
from volume3d_util import *

adjacentIndexOffsets = ((-1,1),(-1,-1),(1,-1),(1,1)) #todo: these probably should be (1, 0), (-1, 0), etc.
adacentIndexOffsets3D = (array((1, 0, 0)), array((0, 1, 0)), array((0, 0, 1)),
                         array((-1, 0, 0)), array((0, -1, 0)), array((0, 0, -1)))

def dijkstra(seedImage):
    """
    Returns the distance to every vertex from the source and the
    array representing, at index i, the node visited before
    visiting node i. This is in the form (dist, previous).
    """
    distanceDataType = float
    NOT_VISITED = finfo(distanceDataType).max
    distanceImage = zeros(seedImage.shape, dtype=distanceDataType)
    distanceImage[:,:] = NOT_VISITED

    visited, queue = {}, []
    for i in range(seedImage.shape[0]):
        for j in range(seedImage.shape[1]):
            if seedImage[i,j]:
                distanceImage[i,j] = 0
                heapq.heappush(queue, (0, (i,j)))

        
            while len(queue) > 0:        distance, current = heapq.heappop(queue)        if current in visited:            continue        visited[current] = True
         #todo: use 4 connected topology (up down left right) to get adjacencies        for offset in adjacentIndexOffsets:            #todo: check if adjacent pixels out of bounds            i = current[0]            j = current[1]            adjacentI = i + offset[0]            adjacentJ = j + offset[1]
            if adjacentI >= 0 and adjacentI < seedImage.shape[0] and adjacentJ >= 0 and adjacentJ < seedImage.shape[1]:                adjNewDistance = distanceImage[i, j] + 1                 adjSavedDistance = distanceImage[adjacentI, adjacentJ]                if adjSavedDistance == NOT_VISITED or adjNewDistance < adjSavedDistance:                    distanceImage[adjacentI, adjacentJ] = adjNewDistance                    heapq.heappush(queue, (adjNewDistance,(adjacentI, adjacentJ)))
    return distanceImage


def floodFill(volume, startPoint):
    """
    Floods the volume starting at the startPoint and returns a list of points
    that represent all of the flooded voxels.
    """

    visitedDict = {}
    visitedList = []
    pointsThatNeedToBeVisited = [(startPoint[0], startPoint[1], startPoint[2])]
    startPointValue = volume[startPoint[0], startPoint[1], startPoint[2]]
    
    while len(pointsThatNeedToBeVisited) > 0:
        point = pointsThatNeedToBeVisited.pop()
        visitedDict[(point[0], point[1], point[2])] = True
        visitedList.append(point)
        for offset in adacentIndexOffsets3D:
            newPointNumpyArray = array(point) + offset
            newPoint = (newPointNumpyArray[0], newPointNumpyArray[1], newPointNumpyArray[2])
            i, j, k = newPoint
            if isInsideVolume(volume, newPoint):
                if (volume[i, j, k] == startPointValue) and (not ((i, j, k) in visitedDict)):
                    pointsThatNeedToBeVisited.append(newPoint)
        
    return visitedList

