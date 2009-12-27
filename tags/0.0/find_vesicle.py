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


from cytoseg_classify import *
#from mitochondria import *
from contour_processing import *

import sys

#from enthought.mayavi.scripts import mayavi2

from default_path import *




def findVesicles(originalVolume):
    
    return findContours(originalVolume, vesicleProbability, contourFilterFunction2D=higherThanSurroundingPixelsFilter, minPerimeter=1, maxPerimeter=50)


def findVesiclesTest():
    
    originalVolume = loadImageStack(driveName + "/images/HPFcere_vol/HPF_rotated_tif/8bit", None)
    
    originalVolume = originalVolume[:,:,3:]
    
    frm.addVolumeAndRefreshDataTree(originalVolume, "OriginalVolume")

    lastZ = 5
    #lastZ = originalVolume.shape[2]
    contourList = findVesicles(originalVolume[:,:,0:lastZ])

    #for contour in contourList:
    #    print contour.features

    

defaultStepNumber = 0

if len(sys.argv) < 2:
    print "step not specified, using default step", defaultStepNumber
    stepNumber = defaultStepNumber
else:
    stepNumber = int(sys.argv[1])    

print "running step number", stepNumber

app = wx.PySimpleApp()
frm = ClassificationControlsFrame(makeClassifyGUITree(), temporaryDataFolder)
frm.Show()

print "starting find"
if stepNumber == 0: findVesiclesTest()

print "finished find"
app.MainLoop()

