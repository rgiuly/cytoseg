
from active_contour import *
from default_path import *
import os

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

exampleSeedPoints = ((81, 114),)
resultImage1 = shellActiveContour(reader.GetOutput(), exampleSeedPoints, 24)
exampleSeedPoints = ((144, 198),)
resultImage2 = shellActiveContour(reader.GetOutput(), exampleSeedPoints, 24)

#filename = os.path.join(defaultOutputPath, "activeContourResult.nrrd")
#print "writing", filename
print "writing to", defaultOutputPath
itk.write(resultImage1, os.path.join(defaultOutputPath, "activeContourResult1.nrrd"))
itk.write(resultImage2, os.path.join(defaultOutputPath, "activeContourResult2.nrrd"))
print "finished writing"


