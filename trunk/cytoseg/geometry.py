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

import copy
import numpy.linalg
from numpy import *

#define MIN(x,y) (x < y ? x : y)
#define MAX(x,y) (x > y ? x : y)
#define INSIDE 0
#define OUTSIDE 1

#typedef struct {
#   double x,y;
#} Point;




def insidePolygon(polygonPoints,p):
  counter = 0;
  #double xinters;
  #Point p1,p2;
  N = len(polygonPoints)
  p1 = polygonPoints[0];
  for i in range(1, N+1):
    p2 = polygonPoints[i % N];
    if (p[1] > min(p1[1],p2[1])):
      if (p[1] <= max(p1[1],p2[1])):
        if (p[0] <= max(p1[0],p2[0])):
          if (p1[1] != p2[1]):
            xinters = (p[1]-p1[1])*(p2[0]-p1[0])/(p2[1]-p1[1])+p1[0]
            if (p1[0] == p2[0] or p[0] <= xinters):
              counter += 1
    #p1 = copy.deepcopy(p2);
    p1 = p2


  if ((counter % 2) == 0):
    return False
  else:
    return True


#def test():
#    polygonPoints = [[0,0],[10,0],[10,10],[0,10]]
#    print insidePolygon(polygonPoints, [.5,.5])
#    print insidePolygon(polygonPoints, [-1,.5])

    
#test()
    
    
    
def distance(vector1,vector2):
    return numpy.linalg.norm(vector2-vector1)


def centerPoint(point1, point2):
    return (array(point1) + array(point2)) / 2.0


def unitVectorFromPoints(startPoint, endPoint):
    return (endPoint - startPoint) / distance(startPoint, endPoint)

