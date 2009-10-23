
#     INPUTS: BrainProtonDensitySlice.png
#     OUTPUTS: FastMarchingImageFilterOutput5.png
#     81 114 1.0  -0.5  3.0   100 100
# 
#     INPUTS: BrainProtonDensitySlice.png
#     OUTPUTS: FastMarchingImageFilterOutput6.png
#     99 114 1.0  -0.5  3.0   100 100
# 
#     INPUTS: BrainProtonDensitySlice.png
#     OUTPUTS: FastMarchingImageFilterOutput7.png
#     56 92 1.0  -0.3  2.0   200 100
# 
#     INPUTS: BrainProtonDensitySlice.png
#     OUTPUTS: FastMarchingImageFilterOutput8.png
#     OUTPUTS: [FastMarchingFilterOutput1.png]
#     OUTPUTS: [FastMarchingFilterOutput2.png]
#     OUTPUTS: [FastMarchingFilterOutput3.png]
#     40 90 0.5  -0.3  2.0   200 100

import itk
from sys import argv, stderr, exit

from numpy import *

from contour_processing import *

from segmentation import floodFill

from tree import getNode

from active_contour import *

#from default_path import *

import os

def numpyToItkPoint(point):

    return [point[2], point[1], point[0]]
    #return point
    

def fastMarch(image1, center, contour, inputVolume):

    InternalPixelType = itk.F
    Dimension = 3
    ImageType = itk.Image[InternalPixelType, Dimension]
    converter = itk.PyBuffer[ImageType]
    IT = itk.Image.F3
    #img = IT.New(Regions=[inputVolume1.shape[2], inputVolume1.shape[1], inputVolume1.shape[0]])
    #img.Allocate()
    #img.FillBuffer(0)
    InternalImageType = IT
    OutputImageType = IT
    itk.write(image1, "/tmp/hello1.nrrd")
    itk.write(image1, "/tmp/hello2.nrrd")
    seedPosition = numpyToItkPoint(center)

    argv[1:] = ["O:\\images\\HPFcere_vol\\HPF_rotated_tif\\median_then_gaussian_8bit_classified_pixels\\median_then_gaussian_8bit_classified_pixels.nrrd", "o:\\temp\\fastmarch3d.nrrd", 81, 114, 1.0, -0.5, 3.0, 0.4, 0.4]

    if( len(argv) < 10 ):
      print >> stderr, """Missing Parameters
    Usage: FastMarchingImageFilter.py inputImage  outputImage seedX seedY Sigma SigmoidAlpha SigmoidBeta TimeThreshold StoppingValue"""
      exit(1)
      
    
    
    CastFilterType = itk.RescaleIntensityImageFilter[ 
                                InternalImageType, 
                                OutputImageType ]
    
    SmoothingFilterType = itk.CurvatureAnisotropicDiffusionImageFilter[ 
                                InternalImageType, 
                                InternalImageType ]
    
    smoothing = SmoothingFilterType.New()
    
    GradientFilterType = itk.GradientMagnitudeRecursiveGaussianImageFilter[
                                InternalImageType, 
                                InternalImageType ]
    
    SigmoidFilterType = itk.SigmoidImageFilter[
                                InternalImageType, 
                                InternalImageType ]
    
    gradientMagnitude = GradientFilterType.New();
    sigmoid = SigmoidFilterType.New()
    
    sigmoid.SetOutputMinimum(  0.0  )
    sigmoid.SetOutputMaximum(  1.0  )
    
    FastMarchingFilterType = itk.FastMarchingUpwindGradientImageFilter[ InternalImageType, 
                                InternalImageType ]

    NodeType = itk.LevelSetNode[InternalPixelType, Dimension]
    NodeContainer = itk.VectorContainer[itk.UI, NodeType]

    
    stopPoints = NodeContainer.New()
    for pointObject in contour.points():
        stopPointNode = NodeType()
        stopPointNode.SetValue(0) #todo: is this needed
        stopPointNode.SetIndex(numpyToItkPoint(pointObject.loc))
        stopPoints.InsertElement(0, stopPointNode)
    
    fastMarching = FastMarchingFilterType.New()
    fastMarching.SetTargetReachedModeToOneTarget()
    fastMarching.SetTargetOffset(0)
    fastMarching.SetTargetPoints(stopPoints)

    fastMarching.SetInput(image1)
    
    sigma = float( argv[5] )
    
    gradientMagnitude.SetSigma(  sigma  )
    
    alpha =  float( argv[6] )
    beta  =  float( argv[7] )
    
    
    seeds = NodeContainer.New()
    
    
    
    node = NodeType()
    seedValue = 0.0
    
    node.SetValue( seedValue )
    node.SetIndex( seedPosition )
    
    seeds.Initialize();
    seeds.InsertElement( 0, node )
    
    fastMarching.SetTrialPoints(  seeds  );
    
    
    fastMarching.SetOutputSize(inputVolume.GetBufferedRegion().GetSize())
    
    stoppingTime = float( argv[9] )
    
    fastMarching.SetStoppingValue(  stoppingTime  )
    
    print "update"
    fastMarching.Update()
    print "finished update"
    resultItkArray = fastMarching.GetOutput()
    return resultItkArray



def shellActiveContourWrapper(image1, seedList, contour, inputVolume):

    InternalPixelType = itk.F
    Dimension = 3
    ImageType = itk.Image[InternalPixelType, Dimension]
    converter = itk.PyBuffer[ImageType]
    IT = itk.Image.F3
    #img = IT.New(Regions=[inputVolume1.shape[2], inputVolume1.shape[1], inputVolume1.shape[0]])
    #img.Allocate()
    #img.FillBuffer(0)
    InternalImageType = IT
    OutputImageType = IT
    itk.write(image1, os.path.join(defaultOutputPath, "hello1.nrrd"))
    itk.write(image1, os.path.join(defaultOutputPath, "hello2.nrrd"))
    #seedPosition = numpyToItkPoint(center)

    argv[1:] = ["O:\\images\\HPFcere_vol\\HPF_rotated_tif\\median_then_gaussian_8bit_classified_pixels\\median_then_gaussian_8bit_classified_pixels.nrrd", "o:\\temp\\fastmarch3d.nrrd", 81, 114, 1.0, -0.5, 3.0, 0.4, 0.4]

    if( len(argv) < 10 ):
      print >> stderr, """Missing Parameters
    Usage: FastMarchingImageFilter.py inputImage  outputImage seedX seedY Sigma SigmoidAlpha SigmoidBeta TimeThreshold StoppingValue"""
      exit(1)



#    CastFilterType = itk.RescaleIntensityImageFilter[ 
#                                InternalImageType, 
#                                OutputImageType ]
    
#    SmoothingFilterType = itk.CurvatureAnisotropicDiffusionImageFilter[ 
#                                InternalImageType, 
#                                InternalImageType ]
    
#    smoothing = SmoothingFilterType.New()
    
#    GradientFilterType = itk.GradientMagnitudeRecursiveGaussianImageFilter[
#                                InternalImageType, 
#                                InternalImageType ]
    
#    SigmoidFilterType = itk.SigmoidImageFilter[
#                                InternalImageType, 
#                                InternalImageType ]
    
#    gradientMagnitude = GradientFilterType.New();
#    sigmoid = SigmoidFilterType.New()
    
#    sigmoid.SetOutputMinimum(  0.0  )
#    sigmoid.SetOutputMaximum(  1.0  )
    
#    FastMarchingFilterType = itk.FastMarchingUpwindGradientImageFilter[ InternalImageType, 
#                                InternalImageType ]

    NodeType = itk.LevelSetNode[InternalPixelType, Dimension]
    NodeContainer = itk.VectorContainer[itk.UI, NodeType]

    
#    stopPoints = NodeContainer.New()
#    for pointObject in contour.points():
#        stopPointNode = NodeType()
#        stopPointNode.SetValue(0) #todo: is this needed
#        stopPointNode.SetIndex(numpyToItkPoint(pointObject.loc))
#        stopPoints.InsertElement(0, stopPointNode)
    
#    fastMarching = FastMarchingFilterType.New()
#    fastMarching.SetTargetReachedModeToOneTarget()
#    fastMarching.SetTargetOffset(0)
#    fastMarching.SetTargetPoints(stopPoints)

#    fastMarching.SetInput(image1)
    
#    sigma = float( argv[5] )
    
#    gradientMagnitude.SetSigma(  sigma  )
    
#    alpha =  float( argv[6] )
#    beta  =  float( argv[7] )
    
    
    #seeds = NodeContainer.New()
    itkSeedList = []

    for point in seedList:    

        itkSeedList.append(numpyToItkPoint(point))

#        node = NodeType()
#        seedValue = 0.0
#        
#        node.SetValue(seedValue)
#        node.SetIndex(numpyToItkPoint(point))
#        
#        seeds.Initialize();
#        seeds.InsertElement(0, node)
    
#    fastMarching.SetTrialPoints(  seeds  );
    
    
#    fastMarching.SetOutputSize(inputVolume.GetBufferedRegion().GetSize())
    
    #stoppingTime = float( argv[9] )
    
    #fastMarching.SetStoppingValue(  stoppingTime  )
    
    resultItkArray = shellActiveContour(inputImage=image1,
                                        seedPoints=itkSeedList,
                                        advectionScaling=80.0,
                                        curvatureScaling=0.75,
                                        dimensions=3)
                                        #advectionScaling=20.0,
                                        #curvatureScaling=1.2,
    
    print "update"
#    fastMarching.Update()
    print "finished update"
#    resultItkArray = fastMarching.GetOutput()
    return resultItkArray


#def fastMarch(inputNumpyVolume, seedPositionNumpyArray, numpyTargetPointList):
#def fastMarch(inputVolume, seedPositionNumpyArray, numpyTargetPointList):
def fastMarch_old(seedPositionNumpyArray, numpyTargetPointList):
    
    if 1:
        seedPosition = numpyToItkPoint(seedPositionNumpyArray)
    
        ImageType = itk.Image[itk.F, 3]
        converter = itk.PyBuffer[ImageType]
        
        #UCImageType = itk.Image[itk.UC, 3]
        #UCConverter = itk.PyBuffer[UCImageType]
    
        print "fast march inputNumpyVolume", numpyBufferFromPyBufferClass
        inputVolume = converter.GetImageFromArray(numpyBufferFromPyBufferClass)
        print "fast march inputVolume", inputVolume
        itk.write(inputVolume, "/tmp/hello.nrrd")
    
        #argv[1:] = ["O:\\software\\InsightToolkit-3.12.0\\Wrapping\\WrapITK\\images\\BrainProtonDensitySlice.png", "o:\\temp\\fastmarch2d.png", 81, 114, 1.0, -0.5, 3.0, 100, 100]
        #argv[1:] = ["O:\\temp\\3dvolume\\3d.nrrd", "o:\\temp\\fastmarch3d.nrrd", 81, 114, 1.0, -0.5, 3.0, 100, 100]
        #argv[1:] = ["O:\\images\\HPFcere_vol\\HPF_rotated_tif\\median_then_gaussian_filter.nrrd", "o:\\temp\\fastmarch3d.nrrd", 81, 114, 1.0, -0.5, 3.0, 100, 100]
        #argv[1:] = ["O:\\images\\HPFcere_vol\\HPF_rotated_tif\\median_then_gaussian_filter.nrrd", "o:\\temp\\fastmarch3d.nrrd", 81, 114, 1.0, -0.5, 3.0, 1, 1]
        #argv[1:] = ["O:\\images\\HPFcere_vol\\HPF_rotated_tif\\median_then_gaussian_8bit_classified_pixels\\median_then_gaussian_8bit_classified_pixels.nrrd", "o:\\temp\\fastmarch3d.nrrd", 81, 114, 1.0, -0.5, 3.0, 0.1, 0.1]
        argv[1:] = ["O:\\images\\HPFcere_vol\\HPF_rotated_tif\\median_then_gaussian_8bit_classified_pixels\\median_then_gaussian_8bit_classified_pixels.nrrd", "o:\\temp\\fastmarch3d.nrrd", 81, 114, 1.0, -0.5, 3.0, 0.4, 0.4]
    
        if( len(argv) < 10 ):
          print >> stderr, """Missing Parameters
        Usage: FastMarchingImageFilter.py inputImage  outputImage seedX seedY Sigma SigmoidAlpha SigmoidBeta TimeThreshold StoppingValue"""
          exit(1)
          
        #itk.auto_progress(2)
        
        
        InternalPixelType = itk.F
        Dimension = 3
        InternalImageType = itk.Image[ InternalPixelType, Dimension ]
        
        OutputPixelType = itk.UC
        OutputImageType = itk.Image[ OutputPixelType, Dimension ]
        
    #    thresholder = itk.BinaryThresholdImageFilter[ InternalImageType, OutputImageType ].New();
    #    
    #    timeThreshold = float( argv[8] )
    #    thresholder.SetLowerThreshold(           0.0  )
    #    thresholder.SetUpperThreshold( timeThreshold  )
    #    
    #    thresholder.SetOutsideValue(  0  )
    #    thresholder.SetInsideValue(  255 )
    #    
    #    ReaderType = itk.ImageFileReader[ InternalImageType ]
    #    WriterType = itk.ImageFileWriter[ OutputImageType ]
    #    
    #    reader = ReaderType.New()
    #    writer = WriterType.New()
    #    
    #    reader.SetFileName( argv[1] )
    #    writer.SetFileName( argv[2] )
        
        
        CastFilterType = itk.RescaleIntensityImageFilter[ 
                                    InternalImageType, 
                                    OutputImageType ]
        
        SmoothingFilterType = itk.CurvatureAnisotropicDiffusionImageFilter[ 
                                    InternalImageType, 
                                    InternalImageType ]
        
        smoothing = SmoothingFilterType.New()
        
        GradientFilterType = itk.GradientMagnitudeRecursiveGaussianImageFilter[
                                    InternalImageType, 
                                    InternalImageType ]
        
        SigmoidFilterType = itk.SigmoidImageFilter[
                                    InternalImageType, 
                                    InternalImageType ]
        
        gradientMagnitude = GradientFilterType.New();
        sigmoid = SigmoidFilterType.New()
        
        sigmoid.SetOutputMinimum(  0.0  )
        sigmoid.SetOutputMaximum(  1.0  )
        
        FastMarchingFilterType = itk.FastMarchingUpwindGradientImageFilter[ InternalImageType, 
                                    InternalImageType ]
        #FastMarchingFilterType = itk.FastMarchingImageFilter[ InternalImageType, 
        #                            InternalImageType ]
    
        NodeType = itk.LevelSetNode[InternalPixelType, Dimension]
        NodeContainer = itk.VectorContainer[itk.UI, NodeType]
    
        #numpyStopPointList = [array(seedPosition) + array([10,10,10])]
        numpyStopPointList = numpyTargetPointList
    
        #print numpyStopPointList
        
        stopPoints = NodeContainer.New()
        for pointObject in numpyStopPointList:
            stopPointNode = NodeType()
            stopPointNode.SetValue(0) #todo: is this needed
            stopPointNode.SetIndex(numpyToItkPoint(pointObject.loc))
            stopPoints.InsertElement(0, stopPointNode)
        
        fastMarching = FastMarchingFilterType.New()
        fastMarching.SetTargetReachedModeToOneTarget()
        fastMarching.SetTargetOffset(0)
        fastMarching.SetTargetPoints(stopPoints)
    
    #    iterationCommand = itk.PyCommand.New()
    #    iterationCommand.SetCommandCallable(fastMarchIterationUpdate)
    #    fastMarching.AddObserver(itk.IterationEvent(), iterationCommand.GetPointer())
        
        #smoothing.SetInput( reader.GetOutput() )
        ##smoothing.SetInput(inputVolume)
        
        ##gradientMagnitude.SetInput( smoothing.GetOutput() )
        ##sigmoid.SetInput( gradientMagnitude.GetOutput() )
        #sigmoid.SetInput( smoothing.GetOutput() )
        #fastMarching.SetInput( sigmoid.GetOutput() )
        #fastMarching.SetInput( smoothing.GetOutput() )
        fastMarching.SetInput(inputVolume)
        #thresholder.SetInput( fastMarching.GetOutput() )
        #writer.SetInput( thresholder.GetOutput() )
        
        ##smoothing.SetTimeStep( 0.125 )
        ##smoothing.SetNumberOfIterations(  5 )
        ##smoothing.SetConductanceParameter( 9.0 )
        
        sigma = float( argv[5] )
        
        gradientMagnitude.SetSigma(  sigma  )
        
        alpha =  float( argv[6] )
        beta  =  float( argv[7] )
        
        ##sigmoid.SetAlpha( alpha )
        ##sigmoid.SetBeta(  beta  )
        
        seeds = NodeContainer.New()
        
        #seedPosition = [10, 10, 10]
        
        
        node = NodeType()
        seedValue = 0.0
        
        node.SetValue( seedValue )
        node.SetIndex( seedPosition )
        #print "fastmarch seed position", seedPosition
        
        seeds.Initialize();
        seeds.InsertElement( 0, node )
        
        fastMarching.SetTrialPoints(  seeds  );
        
        
        #fastMarching.SetOutputSize( 
        #        reader.GetOutput().GetBufferedRegion().GetSize() )
        fastMarching.SetOutputSize(inputVolume.GetBufferedRegion().GetSize())
        
        stoppingTime = float( argv[9] )
        #stoppingTime = float(1000000)
        
        fastMarching.SetStoppingValue(  stoppingTime  )
        
        #writer.Update()
        
        #return UCConverter.GetArrayFromImage(thresholder.GetOutput())
        fastMarching.Update()
        resultItkArray = fastMarching.GetOutput()
        #itk.write(resultItkArray, "/tmp/result.nrrd")
    print "inputVolume2", inputVolume
    itk.write(inputVolume, "/tmp/result_something.nrrd")
    #resultNumpyArray = numpy.array(converter.GetArrayFromImage(resultItkArray))
    #resultNumpyArray = converter.GetArrayFromImage(resultItkArray)
    ##resultItkArray.Delete()
    #inputVolume.Delete()
    #return resultNumpyArray
    
    
#def fastMarchIterationUpdate():
#    
#    print "update"



def shellActiveContourWrapper_old(seedPositionNumpyArray, numpyTargetPointList):
    
    if 1:
        seedPosition = numpyToItkPoint(seedPositionNumpyArray)
    
        ImageType = itk.Image[itk.F, 3]
        converter = itk.PyBuffer[ImageType]
        
        print "fast march inputNumpyVolume", numpyBufferFromPyBufferClass
        inputVolume = converter.GetImageFromArray(numpyBufferFromPyBufferClass)
        print "fast march inputVolume", inputVolume
        itk.write(inputVolume, "/tmp/hello.nrrd")
    
        argv[1:] = ["O:\\images\\HPFcere_vol\\HPF_rotated_tif\\median_then_gaussian_8bit_classified_pixels\\median_then_gaussian_8bit_classified_pixels.nrrd", "o:\\temp\\fastmarch3d.nrrd", 81, 114, 1.0, -0.5, 3.0, 0.4, 0.4]
    
        if( len(argv) < 10 ):
          print >> stderr, """Missing Parameters
        Usage: FastMarchingImageFilter.py inputImage  outputImage seedX seedY Sigma SigmoidAlpha SigmoidBeta TimeThreshold StoppingValue"""
          exit(1)
          
        InternalPixelType = itk.F
        Dimension = 3
        InternalImageType = itk.Image[ InternalPixelType, Dimension ]
        
        OutputPixelType = itk.UC
        OutputImageType = itk.Image[ OutputPixelType, Dimension ]
        
        CastFilterType = itk.RescaleIntensityImageFilter[ 
                                    InternalImageType, 
                                    OutputImageType ]
        
        SmoothingFilterType = itk.CurvatureAnisotropicDiffusionImageFilter[ 
                                    InternalImageType, 
                                    InternalImageType ]
        
        smoothing = SmoothingFilterType.New()
        
        GradientFilterType = itk.GradientMagnitudeRecursiveGaussianImageFilter[
                                    InternalImageType, 
                                    InternalImageType ]
        
        SigmoidFilterType = itk.SigmoidImageFilter[
                                    InternalImageType, 
                                    InternalImageType ]
        
        gradientMagnitude = GradientFilterType.New();
        sigmoid = SigmoidFilterType.New()
        
        sigmoid.SetOutputMinimum(  0.0  )
        sigmoid.SetOutputMaximum(  1.0  )
        
        FastMarchingFilterType = itk.FastMarchingUpwindGradientImageFilter[ InternalImageType, 
                                    InternalImageType ]
    
        NodeType = itk.LevelSetNode[InternalPixelType, Dimension]
        NodeContainer = itk.VectorContainer[itk.UI, NodeType]
    
        numpyStopPointList = numpyTargetPointList
    
        stopPoints = NodeContainer.New()
        for pointObject in numpyStopPointList:
            stopPointNode = NodeType()
            stopPointNode.SetValue(0) #todo: is this needed
            stopPointNode.SetIndex(numpyToItkPoint(pointObject.loc))
            stopPoints.InsertElement(0, stopPointNode)
        
        fastMarching = FastMarchingFilterType.New()
        fastMarching.SetTargetReachedModeToOneTarget()
        fastMarching.SetTargetOffset(0)
        fastMarching.SetTargetPoints(stopPoints)
    
        fastMarching.SetInput(inputVolume)
        
        sigma = float( argv[5] )
        
        gradientMagnitude.SetSigma(  sigma  )
        
        alpha =  float( argv[6] )
        beta  =  float( argv[7] )
        
        seeds = NodeContainer.New()
        
        node = NodeType()
        seedValue = 0.0
        
        node.SetValue( seedValue )
        node.SetIndex( seedPosition )
        
        seeds.Initialize();
        seeds.InsertElement( 0, node )
        
        fastMarching.SetTrialPoints(  seeds  );
        
        
        fastMarching.SetOutputSize(inputVolume.GetBufferedRegion().GetSize())
        
        stoppingTime = float( argv[9] )
        
        fastMarching.SetStoppingValue(  stoppingTime  )
        
        fastMarching.Update()
        resultItkArray = fastMarching.GetOutput()
    print "inputVolume2", inputVolume
    itk.write(inputVolume, "/tmp/result_something.nrrd")



def computeFillFromEllipseCenters(inputVolume1, contourList, fillMethod):

    global numpyBufferFromPyBufferClass
    global img

    InternalPixelType = itk.F
    Dimension = 3
    ImageType = itk.Image[InternalPixelType, Dimension]
    converter = itk.PyBuffer[ImageType]
    IT = itk.Image.F3
    img = IT.New(Regions=[inputVolume1.shape[2], inputVolume1.shape[1], inputVolume1.shape[0]])
    img.Allocate()
    img.FillBuffer(0)
    InternalImageType = IT
    OutputImageType = IT

    numpyBufferFromPyBufferClass = itk.PyBuffer[IT].GetArrayFromImage(img)
    numpyBufferFromPyBufferClass[:, :, :] = inputVolume1
    
    count = 0
    for contour in contourList:
        center = contour.bestFitEllipse.center
        print "compute fill", count, "total", len(contourList)
    
        inputVolume = converter.GetImageFromArray(numpyBufferFromPyBufferClass)
        inputVolumeFileName = os.path.join(defaultOutputPath, "hello.nrrd")
        itk.write(inputVolume, inputVolumeFileName)
        reader1 = itk.ImageFileReader[InternalImageType].New(FileName=inputVolumeFileName)
        image1  = reader1.GetOutput()

        if fillMethod == 'fastMarch':
            resultItkArray = fastMarch(image1, center, contour, inputVolume)
        elif fillMethod == 'shellActiveContour':
            resultItkArray = shellActiveContourWrapper(image1, center, contour, inputVolume)
        else: raise Exception, "Invalid fill method"
        
        tempFileName = os.path.join(defaultOutputPath, "fillResult.nrrd")
        print "writing file", tempFileName
        itk.write(resultItkArray, tempFileName)

        resultVolume = numpy.array(converter.GetArrayFromImage(resultItkArray))
        if 1:
            #contour.features['fastMarchFromEllipseCenter'] = resultVolume
            blob = Blob()
            #binaryResult = resultVolume < 10000000
            binaryResult = resultVolume < 0.5
            if 0:
                print "starting flood fill"
                pointList = floodFill(binaryResult, center)
                print "flood fill finished"
                blob.setPoints(pointList)

            if count == 0:
                sumVolume = (1.0 * binaryResult)
            else:
                sumVolume += (1.0 * binaryResult)

            #contour.features['fastMarchBlobFromEllipseCenter'] = blob
            print "result volume"
        count += 1

    return sumVolume


def quickComputeFillFromEllipseCenters(inputVolume1, contourList, fillMethod):

    global numpyBufferFromPyBufferClass
    global img

    InternalPixelType = itk.F
    Dimension = 3
    ImageType = itk.Image[InternalPixelType, Dimension]
    converter = itk.PyBuffer[ImageType]
    IT = itk.Image.F3
    img = IT.New(Regions=[inputVolume1.shape[2], inputVolume1.shape[1], inputVolume1.shape[0]])
    img.Allocate()
    img.FillBuffer(0)
    InternalImageType = IT
    OutputImageType = IT

    numpyBufferFromPyBufferClass = itk.PyBuffer[IT].GetArrayFromImage(img)
    numpyBufferFromPyBufferClass[:, :, :] = inputVolume1
    
    centerList = []

    for contour in contourList:
        center = contour.bestFitEllipse.center
        centerList.append(center)
        for point in contour.locations():
            centerList.append(((array(point) - array(center)) / 2.0) + array(center))

    count = 0

    center = contour.bestFitEllipse.center
    print "compute fill", count, "total", len(contourList)

    inputVolume = converter.GetImageFromArray(numpyBufferFromPyBufferClass)
    inputVolumeFileName = os.path.join(defaultOutputPath, "hello.nrrd")
    itk.write(inputVolume, inputVolumeFileName)
    reader1 = itk.ImageFileReader[InternalImageType].New(FileName=inputVolumeFileName)
    image1  = reader1.GetOutput()

    if fillMethod == 'fastMarch':
        #resultItkArray = fastMarch(image1, center, contour, inputVolume)
        raise Exception, "not implemented"
    elif fillMethod == 'shellActiveContour':
        resultItkArray = shellActiveContourWrapper(image1, centerList, contour, inputVolume)
    else: raise Exception, "Invalid fill method"
    
    tempFileName = os.path.join(defaultOutputPath, "fillResult.nrrd")
    print "writing file", tempFileName
    itk.write(resultItkArray, tempFileName)

    resultVolume = numpy.array(converter.GetArrayFromImage(resultItkArray))
    if 1:
        #contour.features['fastMarchFromEllipseCenter'] = resultVolume
        blob = Blob()
        #binaryResult = resultVolume < 10000000
        binaryResult = resultVolume < 0.5
        if 0:
            print "starting flood fill"
            pointList = floodFill(binaryResult, center)
            print "flood fill finished"
            blob.setPoints(pointList)

        if count == 0:
            sumVolume = (1.0 * binaryResult)
        else:
            sumVolume += (1.0 * binaryResult)

        #contour.features['fastMarchBlobFromEllipseCenter'] = blob
        print "result volume"
    count += 1

    return sumVolume


def fillAndDisplayResults(gui, inputVolumeName, contoursNodeName,
                          displayParameters, enable3DPlot, fillMethod):
    
    print "fastMarchAndDisplayResults"
    
    numberOfContoursToDisplay = displayParameters.numberOfContoursToDisplay

    inputVolume = gui.getPersistentVolume_old(inputVolumeName)
    #print inputVolume

    node = gui.mainDoc.dataTree.getSubtree((contoursNodeName,))
    #contourList = node.makeChildrenObjectList()
    contourList = nonnullNongroupObjects(node)
    #highProbabilityContourList = highProbabilityContours(contours)
    
    if numberOfContoursToDisplay != None:
        contourList = contourList[0:numberOfContoursToDisplay]


    
    if len(contourList) > 0:

        # perform fast march operations
        #sumVolume = computeFillFromEllipseCenter(inputVolume, contourList, fillMethod)
        sumVolume = quickComputeFillFromEllipseCenters(inputVolume, contourList, fillMethod)
    
        #node = gui.mainDoc.dataTree.writeSubtree((contoursNodeName,))
            # compute the logical or of fastmarches
    #        orVolume = zeros(contourList[0].features['fastMarchFromEllipseCenter'].shape, dtype=int)
    #        count = 0
    #        for contour in contourList:
    #            print "computing logical or of fast march volumes iteration", count
    #            fastMarchVolume = contour.features['fastMarchFromEllipseCenter']
    #            orVolume += (1.0 * (fastMarchVolume < 10000000))
    #            count += 1
        gui.addPersistentVolumeAndRefreshDataTree(sumVolume, inputVolumeName + 'AllFastMarchBlobs')
    
        # display 3D blobs
        if enable3DPlot: displayBlobsFromContourCenters(gui, contourList)
    
        if 0:
            # add blobs for the fastmarch to the data tree
            count = 0
            for contour in contourList:
                gui.addBlob(contour.features['fastMarchBlobFromEllipseCenter'], getNode(gui.mainDoc.dataRootNode, ('Blobs',)), inputVolumeName + ('Blob%d' % count))
                count += 1
    
        gui.mainDoc.dataTree.writeSubtree(('Blobs',))
        gui.refreshTreeControls()
        
    else:
        print "no high probability contours to display"


#@mayavi2.standalone
def displayBlobsFromContourCenters(gui, contourList):

    from enthought.mayavi import mlab as enthought_mlab

    count = 0
    for contour in contourList:
        blobVolume = contour.features['fastMarchFromEllipseCenter']
        enthought_mlab.contour3d(blobVolume, contours=3)
        gui.addVolumeAndRefreshDataTree(blobVolume, 'BlobFromContour%d' % count)
        count += 1    
    
    
