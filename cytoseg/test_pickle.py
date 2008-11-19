#Copyright (c) 2008 by individual cytoseg contributors
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import pickle
import Numeric
import numpy

def writePointList(points, file):
    # save as list of lists because pickling the list of numpy or Numeric arrays doesn't seem to work
    pointList = []
    for p in points:
        coordinateList = []
        for i in range(0,len(p)):
            coordinateList.append(float(p[i]))
        pointList.append(coordinateList)
    pickle.dump(pointList, file)

def readPointList(file):
    points = []
    pointList = pickle.load(file)
    for coordinateList in pointList:
        point = numpy.array(coordinateList)
        points.append(point)
    return points

if 0:
    file = open("temp.pickle", "w")
    b = numpy.array([1,2,3])
    #pickle.dump(b, file)
    b.dump(file)
    file.close()
    blobCenters = b #store in global variable
    
    print 'loadBlobCenters'
    file = open("temp.pickle", "rb")
    #print file
    #blobCenteres = pickle.load(file)
    blobCenters = numpy.load(file)
    print blobCenters
    file.close()


file = open("temp.pickle", "w")
writePointList([numpy.array([1,2]), numpy.array([4,5,6])], file)
#writePointList([[1,2], [4,5,6]], file)
file.close()

file = open("temp.pickle", "rb")
print readPointList(file)
file.close()


def writePointListCSV(points, file):
    # save to comma separated value file
    for p in points:
        for i in range(0,len(p)):
            text = "%f," % p[i]
            file.write(text)
        file.write("\n")
        
file = open("temp.csv", "w")
writePointListCSV([numpy.array([1,2]), numpy.array([4,5,6])], file)
file.close()
        
        




    
