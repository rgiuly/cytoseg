
from numpy import *
import Image
import os


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


def writeTiffStack(path, volume):
    maxValue = 255
    
    a = zeros((volume.shape[0], volume.shape[1]), int8)
    
    #path = 'c:/temp/'
    for i in range(0,volume.shape[2]):

        #a[:,:] = 
        a[:,:] = volume[:,:,i]
        aTransposed = a.T
        image = Image.fromstring("L", (aTransposed.shape[1],aTransposed.shape[0]),
                                 aTransposed.tostring())
        
        
        fullName = os.path.join(path, ('output%0.3d' % i) + '.tif')
        print fullName
        image.save(fullName)


def writeTiffStackRGB(path, redVolume, greenVolume, blueVolume, baseFileName="output"):
    
    if redVolume != None:
        volumeShape = redVolume.shape
    elif greenVolume != None:
        volumeShape = greenVolume.shape
    elif blueVolume != None:
        volumeShape = blueVolume
    else:
        raise Exception, "At least one of the volumes should be a 3D array (all of them are None)."
    
    a = zeros((volumeShape[1], volumeShape[0], 3), dtype=int8)
    
    # todo: check to make sure the three volumes have the same dimensions
    for imageIndex in range(redVolume.shape[2]):
        
        if redVolume != None: a[:,:,0] = redVolume[:,:,imageIndex].T
        if greenVolume != None: a[:,:,1] = greenVolume[:,:,imageIndex].T
        if blueVolume != None: a[:,:,2] = blueVolume[:,:,imageIndex].T
        image = Image.fromarray(a, 'RGB')
        
        fullName = os.path.join(path, ('%s%0.3d%s' % (baseFileName, imageIndex, '.bmp')))
        print fullName
        image.save(fullName)

