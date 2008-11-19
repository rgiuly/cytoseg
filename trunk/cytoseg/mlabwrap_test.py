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


import numpy
#import Numeric
from mlabwrap import mlab
a=[[1.,2.,3.],[4.,5.,6.]]
b=numpy.ones((10,10,10))
b=b*10
b[1,4,6]=1
b[8,8,8]=1
b[8,8,9]=1



def matlabToPythonPointList(matlabPointList):
    newPoints = []
    for point in matlabPointList:
        #print point[0]
        #print point[1]
        #print point[2]
        newPoints.append(numpy.array((point[2]-1, point[0]-1, point[1]-1)))
    return newPoints
    
    

#mlab.sliceView(b)
#mlab.findBlobs(b.flat,[3,3,3],2)
#print mlab.norm(b.flat)
#print mlab.double(b.flat)
#print mlab.findBlobs()

#x, y = mlab.test(nout=2)
#print x
#print y

centroids, areas = mlab.findBlobs(b.flat,5,10,10,10,nout=2)
print 'centroids'
print centroids
print matlabToPythonPointList(centroids)
print 'areas'
print areas


# test to see if flatten and reshape work
#c = numpy.array([[1,2,3,4],[5,6,7,8]])
#d = c.flatten();
#e = mlab.reshape(d,c.shape[1],c.shape[0])

#print c
#print e


def reverseIndices(v):
    v1 = numpy.zeros((v.shape[2],v.shape[1],v.shape[0]))
    for i in range(0,v.shape[0]):
        for j in range(0,v.shape[1]):
            for k in range(0,v.shape[2]):
                v1[k,j,i] = v[i,j,k]
    return v1;

c = numpy.zeros((2,2,2));
#d = numpy.zeros((2,2,2));
c[0,0,0] = 1
c[0,0,1] = 2
c[0,1,0] = 3
c[0,1,1] = 4
c[1,0,0] = 5
c[1,0,1] = 6
c[1,1,0] = 7
c[1,1,1] = 80
d = reverseIndices(c)
            
'reshape and write matrix'            
mlab.reshapeAndWriteMatrix(d.flatten(),2,2,2)










