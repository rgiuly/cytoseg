from numpy import *
import numpy
import geometry
import itk
from containers import *


def gaussian(x, amplitude, sigma):
    return amplitude * exp(-pow(x, 2) / (2*pow(sigma,2)))

# 3D gaussian
global defaultType
defaultType = numpy.float32
def gaussianVolume(shape, position, amplitude, sigma):
    # sigma is fatness
    volume = zeros(shape, defaultType)
    for x in range(0, shape[0]):
        for y in range(0, shape[1]):
            for z in range(0, shape[2]):
                dist = geometry.distance(position, array([x,y,z]))
                #volume[x,y,z] = dist * 20
                volume[x,y,z] = gaussian(dist, amplitude, sigma)
    return volume

#todo: it may be that (N-1)/2.0 is the middle, not N/2.0, where N is dimension
def differenceOfOffsetGaussians(volumeShape, offsetVector, sigma):
    #g0 = gaussianVolume(volumeShape, (array(volumeShape)-1)/2.0 + -array(offsetVector), 1, sigma)
    #g1 = gaussianVolume(volumeShape, (array(volumeShape)-1)/2.0 + array(offsetVector), 1, sigma)
    g0 = gaussianVolume(volumeShape, array(volumeShape)/2 + -array(offsetVector), 1, sigma)
    g1 = gaussianVolume(volumeShape, array(volumeShape)/2 + array(offsetVector), 1, sigma)
    return g0-g1
    #return gaussianVolume(volumeShape, array(volumeShape)/2, 1, sigma)

def differenceOfGaussians(volumeShape, sigma1, sigma2, amplitude1=1.0, amplitude2=1.0):
    center = (array(volumeShape)-1)/2.0
    g1 = gaussianVolume(volumeShape, center, amplitude1, sigma1)
    g2 = gaussianVolume(volumeShape, center, amplitude2, sigma2)
    return g1-g2


def makeItkImage(dimensions, pixelType):
    Dimension = 2
    ImageType = itk.Image[pixelType, Dimension]
    
    index = itk.Index[2]()
    index.SetElement(0,0)
    index.SetElement(1,0)
    
    size = itk.Size[2]()
    size.SetElement(0, dimensions[0])
    size.SetElement(1, dimensions[1])
    
    imageRegion = itk.ImageRegion[2]()
    imageRegion.SetSize(size)
    imageRegion.SetIndex(index)
    
    
    image = ImageType.New()
    #image.SetSize([10,10])
    #image.SetIndex([0,0])
    #image.SetPixel([0,0], 0)
    
    image.SetRegions(imageRegion)
    image.Allocate()
    image.FillBuffer(0)
    
    return image

def numpyToItk(numpyArray):

    itkImage = makeItkImage(numpyArray.shape, itk.F)

    index = [None, None]
    for i in range(numpyArray.shape[0]):
        for j in range(numpyArray.shape[1]):
            index[0] = i
            index[1] = j
            itkImage.SetPixel(index, numpyArray[i,j])

    return itkImage

    
def itkToNumpy(itkImage):

    region = itkImage.GetLargestPossibleRegion()
    size = region.GetSize()
    
    numpyArray = zeros((size.GetElement(0), size.GetElement(1)), dtype=float)

    index = [None, None]
    for i in range(size.GetElement(0)):
        for j in range(size.GetElement(1)):
            index[0] = i
            index[1] = j
            numpyArray[i,j] = itkImage.GetPixel(index)

    return numpyArray


def secondDerivatives2D(numpyArray2D):
    
    inputImage = numpyToItk(numpyArray2D)
    PixelType = itk.F
    Dimension = 2
    ImageType = itk.Image[PixelType, Dimension]
    #DuplicatorType = itk.ImageDuplicator[OutputImageType]
    FilterType = itk.RecursiveGaussianImageFilter[ImageType, ImageType]

    sigma = 3

    #duplicator = DuplicatorType.New()

    ga = FilterType.New()
    gb = FilterType.New()
    ga.SetSigma(sigma)
    gb.SetSigma(sigma)

    ga.SetDirection(0) # x direction
    gb.SetDirection(1) # y direction
    ga.SetSecondOrder()
    gb.SetZeroOrder()

    ga.SetInput(inputImage)
    gb.SetInput(ga.GetOutput())
    
    gb.Update()

    hessian = odict()
    hessian['xx'] = itkToNumpy(gb.GetOutput()) 

    ga.SetZeroOrder()
    gb.SetSecondOrder()
    gb.Update()
    hessian['yy'] = itkToNumpy(gb.GetOutput()) 

    ga.SetFirstOrder()
    gb.SetFirstOrder()
    gb.Update()
    hessian['xy'] = itkToNumpy(gb.GetOutput()) 

    ga.SetDirection(1) # y direction
    gb.SetDirection(0) # x direction
    ga.SetFirstOrder()
    gb.SetFirstOrder()
    gb.Update()
    hessian['yx'] = itkToNumpy(gb.GetOutput()) 
    
    return hessian

    #duplicator->SetInputImage(gb->GetOutput());

    #gb->Update(); # probably not needed
    #duplicator->Update();

    #Ixx = duplicator->GetOutput();



#
#    gc->SetDirection( 1 );  // gc now works along Y
#    gb->SetDirection( 2 );  // gb now works along Z
#
#    gc->Update();
#    duplicator->Update();
#
#    ImageType::Pointer Iyy = duplicator->GetOutput();
#
#    writer->SetInput( Iyy );
#    outputFileName = outputPrefix + "-Iyy.mhd";
#    writer->SetFileName( outputFileName.c_str() );
#    writer->Update();
#
#
#    gc->SetDirection( 0 );  // gc now works along X
#    ga->SetDirection( 1 );  // ga now works along Y
#
#    gc->Update();
#    duplicator->Update();
#
#    ImageType::Pointer Ixx = duplicator->GetOutput();
#
#    writer->SetInput( Ixx );
#    outputFileName = outputPrefix + "-Ixx.mhd";
#    writer->SetFileName( outputFileName.c_str() );
#    writer->Update();
#
#
#    ga->SetDirection( 0 );
#    gb->SetDirection( 1 );
#    gc->SetDirection( 2 );
#
#    ga->SetZeroOrder();
#    gb->SetFirstOrder();
#    gc->SetFirstOrder();
#
#    gc->Update();
#    duplicator->Update();
#
#    ImageType::Pointer Iyz = duplicator->GetOutput();
#
#    writer->SetInput( Iyz );
#    outputFileName = outputPrefix + "-Iyz.mhd";
#    writer->SetFileName( outputFileName.c_str() );
#    writer->Update();
#
#
#    ga->SetDirection( 1 );
#    gb->SetDirection( 0 );
#    gc->SetDirection( 2 );
#
#    ga->SetZeroOrder();
#    gb->SetFirstOrder();
#    gc->SetFirstOrder();
#
#    gc->Update();
#    duplicator->Update();
#
#    ImageType::Pointer Ixz = duplicator->GetOutput();
#
#    writer->SetInput( Ixz );
#    outputFileName = outputPrefix + "-Ixz.mhd";
#    writer->SetFileName( outputFileName.c_str() );
#    writer->Update();
#
#    ga->SetDirection( 2 );
#    gb->SetDirection( 0 );
#    gc->SetDirection( 1 );
#
#    ga->SetZeroOrder();
#    gb->SetFirstOrder();
#    gc->SetFirstOrder();
#
#    gc->Update();
#    duplicator->Update();
#
#    ImageType::Pointer Ixy = duplicator->GetOutput();
#
#    writer->SetInput( Ixy );
#    outputFileName = outputPrefix + "-Ixy.mhd";
#    writer->SetFileName( outputFileName.c_str() );
#    writer->Update();

def dilateVolume2D(inputVolume):

    InternalPixelType = itk.F
    Dimension = 2
    ImageType = itk.Image[InternalPixelType, Dimension]
    converter = itk.PyBuffer[ImageType]
    
    outputVolume = zeros(inputVolume.shape)
    
    for z in range(inputVolume.shape[2]):
        
        array2d = inputVolume[:,:,z]
        #image2d = converter.GetImageFromArray(array2d)
        image2d = numpyToItk(array2d)
        dim = 2
        kernel = itk.strel(dim, 2)
        dilateFilter = itk.GrayscaleDilateImageFilter[ImageType, ImageType, kernel].New(
                        image2d, Kernel=kernel)
        dilateFilter.Update()
        #outputVolume[:,:,z] = converter.GetArrayFromImage(dilateFilter.GetOutput())
        outputVolume[:,:,z] = itkToNumpy(dilateFilter.GetOutput())

    return outputVolume


