#mlabwrap test

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
from mlabwrap import mlab

#a = numpy.zeros((3,3,3), order='FORTRAN')
a = numpy.zeros((3,3,3))


for x in range(0,3):
    for y in range(0,3):
        for z in range(0,3):
            #a[x,y,z] = 10000 +  x*100 + y*10 + z
            a[x,y,z] = (x+1)*100 + (y+1)*10 + (z+1)


#print mlab.abs(-1)
#mlab.display(-1)
#print a.flatten()
#print mlab.abs(-1)
#print mlab.abs(a.flatten())

# writes output to a file
mlab.mlabwrap_test_3darray_matlab(a.flatten())