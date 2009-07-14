
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

