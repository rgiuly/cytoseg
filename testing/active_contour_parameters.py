
from active_contour import *
from default_path import *
import os
from itk_util import *
from numpy import *
from volume3d_util import *

def frange(start, end=None, inc=None):
    "A range function, that does accept float increments..."

    if end == None:
        end = start + 0.0
        start = 0.0

    if inc == None:
        inc = 1.0

    L = []
    while 1:
        next = start + len(L) * inc
        if inc > 0 and next >= end:
            break
        elif inc < 0 and next <= end:
            break
        L.append(next)
        
    return L

#    InternalPixelType = itk.F
#    Dimension = 2
#    InternalImageType = itk.Image[InternalPixelType, Dimension]
#
#    reader = itk.ImageFileReader[InternalImageType].New(FileName="data/classified_inverted_out0005.png")
#    # needed to give the size to the fastmarching filter
#    reader.Update()

inputFile = "data/classified_inverted_out0005.png"

#OutputImageType = itk.Image[OutputPixelType, Dimension]
InternalPixelType = itk.F
Dimension = 2
InternalImageType = itk.Image[InternalPixelType, Dimension]

reader = itk.ImageFileReader[InternalImageType].New(FileName=inputFile)
# needed to give the size to the fastmarching filter
reader.Update()

#readerOriginal = itk.ImageFileReader[InternalImageType].New(FileName=inputFileOriginal)

#seedPointsList = (((81, 114),), ((144, 198),))
seedPointsList = (((223, 124),), ((144, 198),))
advectionScalingList = frange(10, 14, 1)
#advectionScalingList = (12,)
#propagationScalingList = frange(0.7, 1.5, 0.2)
propagationScalingList = (1.0,)
curvatureScalingList = frange(0.75, 2, 0.4)

for seedPoints in seedPointsList:

    for advectionScalingIndex in range(len(advectionScalingList)):
        advectionScaling = advectionScalingList[advectionScalingIndex]

        for propagationScalingIndex in range(len(propagationScalingList)):
            propagationScaling = propagationScalingList[propagationScalingIndex]

            for curvatureScalingIndex in range(len(curvatureScalingList)):
                curvatureScaling = curvatureScalingList[curvatureScalingIndex]


                resultImage1 = shellActiveContour(reader.GetOutput(),
                                                  seedPoints=seedPoints,
                                                  advectionScaling=advectionScaling,
                                                  propagationScaling=propagationScaling,
                                                  curvatureScaling=curvatureScaling)
                
                #filename = os.path.join(defaultOutputPath, "activeContourResult.nrrd")
                #print "writing", filename
#                filename = "%s_advection=%s_propagation=%s_=curvature=%s" % (seedPoints,
#                                            advectionScaling,
#                                            propagationScaling,
#                                            curvatureScaling)
                filename = "%s_%d_%d_%d_" % (seedPoints,
                                            advectionScalingIndex,
                                            propagationScalingIndex,
                                            curvatureScalingIndex)
                print "writing to", defaultOutputPath
                rescaleAndWrite(resultImage1, os.path.join(defaultOutputPath, "activeContour" +
                                                     filename + ".tif"))
                print "finished writing"

                InternalPixelType = itk.F
                Dimension = 2
                ImageType = itk.Image[InternalPixelType, Dimension]
                converter = itk.PyBuffer[ImageType]
                original = converter.GetArrayFromImage(reader.GetOutput())
                original = original[160:250, 90:190]
                array = converter.GetArrayFromImage(resultImage1)
                array = array[160:250, 90:190]
                originalVolume = zeros((original.shape[0], original.shape[1], 1))
                originalVolume[:,:,0] = original
                #originalVolume = originalVolume[90:190, 160:250, 0]
                volume = zeros((array.shape[0], array.shape[1], 1))
                volume[:,:,0] = array
                #volume = volume[90:190, 160:250, 0]
                print volume.shape
                writeTiffStackRGB("o:/temp/rgb",
                                  baseFileName="out_%s"%filename,
                                  redVolume=volume,
                                  greenVolume=originalVolume,
                                  blueVolume=None)
