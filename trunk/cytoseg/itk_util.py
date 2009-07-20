
import itk

def rescaleAndWrite(filter, fileName):

    InternalPixelType = itk.F
    Dimension = 2
    InternalImageType = itk.Image[InternalPixelType, Dimension]
    
    OutputPixelType = itk.UC
    OutputImageType = itk.Image[OutputPixelType, Dimension]

    caster = itk.RescaleIntensityImageFilter[InternalImageType, OutputImageType].New(filter,
                   OutputMinimum=0,
               OutputMaximum=255)
    itk.write(caster, fileName)

