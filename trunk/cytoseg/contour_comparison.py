
from numpy import *
from geometry import *
from point_set import *

# see Hausdorff distance
def biggestGap(contour1, contour2):

    biggestGapValue = 0

    locations1 = contour1.locations()
    locations2 = contour2.locations()

    for index1 in range(len(locations1)):
        point1 = array(locations1[index1])

        # the minimum distance represents the gap from point1 to point2

        # initialize gap
        gap = distance(point1, array(locations2[0]))

        # find the minimum
        #print "find the minimum"
        for coordList2 in locations2:
            point2 = array(coordList2)
            dist = distance(point1, point2)
            #print dist
            if dist < gap:
                gap = dist

        # if the gap is the largest found so far, keep it
        if gap > biggestGapValue:
            biggestGapValue = gap

    return biggestGapValue


def overlap_old(contour1, contour2):

    temp1 = zeros((1000, 1000), dtype=int8)
    temp2 = zeros((1000, 1000), dtype=int8)

    binaryImage1 = contour1.binaryImage
    binaryImage2 = contour2.binaryImage

    boundingBox1 = contour1.get2DBoundingBox()
    boundingBox2 = contour2.get2DBoundingBox()

    temp1[boundingBox1[0][0]:boundingBox1[1][0]+1,
          boundingBox1[0][1]:boundingBox1[1][1]+1] = binaryImage1

    temp2[boundingBox2[0][0]:boundingBox2[1][0]+1,
          boundingBox2[0][1]:boundingBox2[1][1]+1] = binaryImage2

    andImage = logical_and(temp1, temp2) * 1
    orImage = logical_or(temp1, temp2) * 1
    fraction = float(sum(andImage)) / float(sum(orImage))

    return fraction


def overlap(contour1, contour2):

    #temp1 = zeros((1000, 1000), dtype=int8)
    #temp2 = zeros((1000, 1000), dtype=int8)

    binaryImage1 = contour1.binaryImage
    binaryImage2 = contour2.binaryImage

    boundingBox1 = contour1.get2DBoundingBox()
    boundingBox2 = contour2.get2DBoundingBox()

    minX = min(boundingBox1[0][0], boundingBox2[0][0])
    minY = min(boundingBox1[0][1], boundingBox2[0][1])
    maxX = max(boundingBox1[1][0], boundingBox2[1][0])
    maxY = max(boundingBox1[1][1], boundingBox2[1][1])

    temp1 = zeros((maxX-minX+1, maxY-minY+1))
    temp2 = zeros((maxX-minX+1, maxY-minY+1))

    temp1[boundingBox1[0][0]-minX:boundingBox1[1][0]-minX+1,
          boundingBox1[0][1]-minY:boundingBox1[1][1]-minY+1] = binaryImage1

    temp2[boundingBox2[0][0]-minX:boundingBox2[1][0]-minX+1,
          boundingBox2[0][1]-minY:boundingBox2[1][1]-minY+1] = binaryImage2

    andImage = logical_and(temp1, temp2) * 1
    orImage = logical_or(temp1, temp2) * 1
    fraction = float(sum(andImage)) / float(sum(orImage))

    return fraction

