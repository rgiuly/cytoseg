
from numpy import *
import Image
import os
from scipy import ndimage


class Box:

    def __init__(self, cornerA=None, cornerB=None):
        
        # 3D point
        if cornerA == None:
            self.cornerA = [None, None, None]
        else:
            self.cornerA = list(cornerA)
        
        # 3D point
        if cornerB == None:
            self.cornerB = [None, None, None]
        else:
            self.cornerB = list(cornerB)
        
    def shape(self):
        return array(self.cornerB) - array(self.cornerA)


    # None for an initial parameter mean start from 0
    # None for a final parameter means go to the last index
    def getBoxForShape(self, shape):

        resultBox = Box()

        for coordinateIndex in range(3):
            #print type(self.cornerA[coordinateIndex])
            #print type(self.cornerB[coordinateIndex])
            if self.cornerA[coordinateIndex] == None:
                resultBox.cornerA[coordinateIndex] = 0
            else:
                resultBox.cornerA[coordinateIndex] = self.cornerA[coordinateIndex]
            if self.cornerB[coordinateIndex] == None:
                resultBox.cornerB[coordinateIndex] = shape[coordinateIndex]
            else:
                resultBox.cornerB[coordinateIndex] = self.cornerB[coordinateIndex]

        return resultBox


def isInsideVolume(volume, point):
    s = volume.shape
    if point[0] < s[0] and point[1] < s[1] and point[2] < s[2] and point[0] >= 0 and point[1] >= 0 and point[2] >= 0:
        return True
    else:
        return False


def at(volume, point):
    return volume[point[0],point[1],point[2]]


def rescale(volume, min, max):
    
    factor = float(max - min) / float(volume.max() - volume.min())
    return ((volume - volume.min()) * factor) + min


def resizeVolume(volume, factors):
    
    inputShape = volume.shape
    
    #if type(factor) != type(1):
    #    raise Exception, "Non-integer %s used. Please use an integer." % factor
    
    Nx = ((inputShape[0]-1)*factors[0] + 1) # new number of samples in x direction
    Ny = ((inputShape[1]-1)*factors[1] + 1) # new number of samples in y direction
    Nz = ((inputShape[2]-1)*factors[2] + 1) # new number of samples in z direction

    #todo: use this
    #    coords = mgrid[0:inputShape[0]-1:Nx*1j,
    #                   0:inputShape[1]-1:Ny*1j,
    #                   0:inputShape[2]-1:Nz*1j]
    
    ivals, jvals, kvals = mgrid[0:inputShape[0]-1:Nx*1j,
                                0:inputShape[1]-1:Ny*1j,
                                0:inputShape[2]-1:Nz*1j]
    
    
    coords = array([ivals, jvals, kvals])
    
    newVolume = ndimage.map_coordinates(volume, coords, order=1)
    #newVolume = ndimage.map_coordinates(volume, coords)
    
    return newVolume


# todo: path and filename combining should be done with a function for certain operating system i think
def writeTiffStack_version1(path, redVolume, greenVolume, blueVolume):
    maxValue = 255
    
    #path = 'c:/temp/'
    for i in range(0,redVolume.shape[2]):
        # all the volumes of each color should have the same dimensions (shape)
        colorImageArray = numpy.zeros((redVolume.shape[0], redVolume.shape[1], 3), numpy.uint8)
        
        colorImageArray[:,:,0] = redVolume[:,:,i]
        colorImageArray[:,:,1] = greenVolume[:,:,i]
        colorImageArray[:,:,2] = blueVolume[:,:,i]
        #colorImageArray[:,:,3] = maxValue
        
        #image = Image.fromarray(colorImageArray, 'RGB')
        
        image = Image.fromstring("F", (a.shape[1],a.shape[0]), a.tostring())
        
        
        fullName = path + ('output%0.3d' % i) + '.tiff'
        print fullName
        image.save(fullName)


def writeTiffStack(path, volume, baseFileName="output", startIndex=0):

    maxValue = 255
    
    a = zeros((volume.shape[0], volume.shape[1]), dtype=int8)
    
    #path = 'c:/temp/'
    for i in range(0,volume.shape[2]):

        #a[:,:] = 
        a[:,:] = volume[:,:,i]
        aTransposed = a.T
        image = Image.fromstring("L", (aTransposed.shape[1],aTransposed.shape[0]),
                                 aTransposed.tostring())

        fullName = os.path.join(path,
                    ('%s%0.3d%s' % (baseFileName, startIndex + i, '.tif')))
        print fullName
        image.save(fullName)


def writeTiffStackRGB(path, redVolume, greenVolume, blueVolume,
                      baseFileName="output", startIndex=0):
    
    if redVolume != None:
        volumeShape = redVolume.shape
    elif greenVolume != None:
        volumeShape = greenVolume.shape
    elif blueVolume != None:
        volumeShape = blueVolume
    else:
        raise Exception, "At least one of the volumes should be a 3D array (all of them are None)."
    
    # array for the image
    a = zeros((volumeShape[1], volumeShape[0], 3), dtype=int8)
    
    # todo: check to make sure the three volumes have the same dimensions
    for imageIndex in range(redVolume.shape[2]):
        
        if redVolume != None: a[:,:,0] = redVolume[:,:,imageIndex].T
        if greenVolume != None: a[:,:,1] = greenVolume[:,:,imageIndex].T
        if blueVolume != None: a[:,:,2] = blueVolume[:,:,imageIndex].T
        image = Image.fromarray(a, 'RGB')
        
        fullName = os.path.join(path, ('%s%0.3d%s' % (baseFileName,
                                                      startIndex + imageIndex,
                                                      '.bmp')))
        print fullName
        image.save(fullName)

